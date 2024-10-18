from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import jwt_required, get_jwt_identity
from tables import session, ChatHistory, ChatWindow, User, RelatedQuestions
from agent_setup import setup_agent
from question_agent_setup import setup_question_generator
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc
import logging
import traceback


chat_bp = Blueprint('chat', __name__)
limiter = Limiter(key_func=get_remote_address)

# Chat route with rate limiting and user authentication
@chat_bp.route('/chat', methods=['POST'])
@jwt_required()
@limiter.limit("10 per minute", key_func=get_jwt_identity)
def chat():
    user_input = request.json.get('message')
    chat_window_id = request.json.get('chat_window_id')
    user_id = request.json.get('user_id')


    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    if not chat_window_id:
        return jsonify({"error": "No chat window ID provided"}), 400

    try:
        user = session.query(User).filter_by(user_id=user_id).first()

        # Fetch memory for the chat window (if any previous memory exists)
        db_conversation = get_last_10_messages(user_id=user_id, chat_window_id=chat_window_id)

        agent = setup_agent(db_conversation)
        question_generator = setup_question_generator()
        # Invoke the agent with user input and memory (for context)
        
        agent_response, related_questions = process_query(agent, question_generator, user_input, user_id, chat_window_id)

        agent_response = agent.invoke({"input": user_input})
        logging.info(f"Agent response: {agent_response}")
        
        bot_output = agent_response["output"]

        # Store the chat and update memory
        store_chat(user.user_id, chat_window_id, user_input, bot_output)

        # Return both bot response and related questions
        return jsonify({
            "response": bot_output,
            "related_questions": related_questions
        })

    except Exception as e:
        logging.error(f"Error in chat: {str(e)}")
        logging.error(traceback.format_exc())
        return jsonify({"error": "Internal Server Error"}), 500


def process_query(agent, question_generator, user_input, user_id, chat_window_id):
    # Get the main agent's response
    agent_response = agent.invoke({"input": user_input})

    # Extract the chat history from the agent's memory
    chat_history = "\n".join([f"{msg.type}: {msg.content}" for msg in agent.memory.chat_memory.messages])

    # Generate related questions
    related_questions = question_generator.generate_questions(user_input, chat_history)

    # Save the related questions to the database for the current chat window and user
    for question in related_questions:
        new_related_question = RelatedQuestions(
            chat_window_id=chat_window_id,
            user_id=user_id,  # Include user_id
            question=question
        )
        session.add(new_related_question)

    session.commit()

    return agent_response, related_questions


# Function to store the chat conversation in the database
def store_chat(user_id, chat_window_id, user_message, bot_response):
    try:
        # Store user message
        new_chat_user = ChatHistory(
            user_id=user_id,
            chat_window_id=chat_window_id,
            user_message=user_message,
            bot_response=None,
            sender_role='user',  # Mark this as a user message
        )
        session.add(new_chat_user)
        
        # Store bot response
        new_chat_bot = ChatHistory(
            user_id=user_id,
            chat_window_id=chat_window_id,
            user_message=None,
            bot_response=bot_response,
            sender_role='bot',  # Mark this as a bot message
        )
        session.add(new_chat_bot)
        
        session.commit()
        logging.info("Chat successfully stored in the database")

    except Exception as e:
        session.rollback()  # Rollback in case of error
        logging.error(f"Error storing chat: {str(e)}")
        logging.error(traceback.format_exc())
        raise


@chat_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history(limit=None):
    user_email = get_jwt_identity()  # Get the email from the JWT
    chat_window_id = request.args.get('chat_window_id')  # Get chat window ID from query param
    user = session.query(User).filter_by(email=user_email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not chat_window_id:
        return jsonify({"error": "No chat window ID provided"}), 400

    user_id = user.user_id

    try:
        query = session.query(ChatHistory).filter_by(user_id=user_id, chat_window_id=chat_window_id)
        
        if limit:
            query = query.order_by(desc(ChatHistory.timestamp)).limit(limit)
        
        chats = query.all()

        if limit:
            chats.reverse()  # Reverse to maintain chronological order if limit was applied

        history = [{'message': chat.user_message or chat.bot_response, 'sender_role': chat.sender_role, 'timestamp': chat.timestamp} for chat in chats]
        return jsonify(history)
    except Exception as e:
        logging.error(f"Error fetching chat history: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
    

def get_last_10_messages(user_id, chat_window_id):
    query = session.query(ChatHistory).filter_by(user_id=user_id, chat_window_id=chat_window_id).order_by(desc(ChatHistory.timestamp)).limit(10)
    chats = query.all()

    chats.reverse()
    memory = [chat.user_message or chat.bot_response for chat in chats]

    return memory


def create_new_chat_window(user_id, chat_name):
    try:
        # Create a new chat window with a name
        new_chat_window = ChatWindow(user_id=user_id, name=chat_name)
        session.add(new_chat_window)
        session.commit()

        return new_chat_window.chat_window_id
    except Exception as e:
        session.rollback()
        raise e


@chat_bp.route('/chat-windows', methods=['GET'])
@jwt_required()
def get_chat_windows():
    user_email = get_jwt_identity()  # Get the email from the JWT
    user = session.query(User).filter_by(email=user_email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    limit = request.args.get('limit', default=20, type=int)  # Get the limit parameter from query string
    user_id = user.user_id

    try:
        # Query the latest chat windows for the user that are not soft deleted
        chat_windows = session.query(ChatWindow).filter_by(user_id=user_id, deleted=False).order_by(desc(ChatWindow.created_at)).limit(limit).all()
        
        # Format the chat windows data to include name, id, and created_at
        chat_window_list = [{'id': chat.chat_window_id, 'name': chat.name, 'created_at': chat.created_at} for chat in chat_windows]

        return jsonify(chat_window_list)
    except Exception as e:
        logging.error(f"Error fetching chat windows: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500



@chat_bp.route('/chat-windows', methods=['POST'])
@jwt_required()  # Assuming you have authentication in place
def create_chat_window():
    data = request.get_json()
    chat_name = data.get('name')

    if not chat_name:
        return jsonify({"error": "Chat name is required"}), 400

    user_email = get_jwt_identity()  # Get the user email from JWT
    user = session.query(User).filter_by(email=user_email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Create a new chat window with the provided name
    new_chat_window = ChatWindow(user_id=user.user_id, name=chat_name)
    session.add(new_chat_window)
    session.commit()

    return jsonify({
        'id': new_chat_window.chat_window_id,
        'name': new_chat_window.name,
        'created_at': new_chat_window.created_at
    }), 201


@chat_bp.route('/chat-windows/<int:chat_window_id>/related-questions', methods=['POST'])
@jwt_required()
def add_related_question(chat_window_id):
    user_id = get_jwt_identity()  # Get user ID from JWT
    question = request.json.get('question')

    if not question:
        return jsonify({"error": "No question provided"}), 400

    # Save the related question to the database
    new_question = RelatedQuestions(
        chat_window_id=chat_window_id,
        user_id=user_id,  # Store user ID
        question=question
    )
    session.add(new_question)
    session.commit()

    return jsonify({"message": "Related question added successfully"}), 201


@chat_bp.route('/chat-windows/<int:chat_window_id>/related-questions', methods=['GET'])
@jwt_required()
def get_related_questions(chat_window_id):
    try:
        # Fetch the latest 2 related questions for the specified chat window, ordered by created_at
        related_questions = session.query(RelatedQuestions)\
            .filter_by(chat_window_id=chat_window_id)\
            .order_by(RelatedQuestions.created_at.desc())\
            .limit(2)\
            .all()

        # Return the questions in a JSON response
        return jsonify([{'question': rq.question} for rq in related_questions]), 200
    except Exception as e:
        logging.error(f"Error fetching related questions: {e}")
        return jsonify({"error": "Could not fetch related questions"}), 500


@chat_bp.route('/chat-windows/<int:chat_window_id>', methods=['DELETE'])
@jwt_required()
def delete_chat_window(chat_window_id):
    try:
        # Query the chat window by its ID
        chat_window = session.query(ChatWindow).filter_by(chat_window_id=chat_window_id).first()

        if not chat_window:
            return jsonify({"error": "Chat window not found"}), 404

        # Soft delete by setting the 'deleted' flag to TRUE
        chat_window.deleted = True
        session.commit()

        return jsonify({"message": "Chat window soft deleted successfully"}), 200

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": f"Error deleting chat window: {str(e)}"}), 500


@chat_bp.route('/chat-windows/<int:chat_window_id>', methods=['PUT'])
@jwt_required()
def rename_chat_window(chat_window_id):
    data = request.get_json()
    new_name = data.get('name')

    if not new_name:
        return jsonify({"error": "Chat window name is required"}), 400

    try:
        # Query the chat window by its ID
        chat_window = session.query(ChatWindow).filter_by(chat_window_id=chat_window_id, deleted=False).first()

        if not chat_window:
            return jsonify({"error": "Chat window not found or already deleted"}), 404

        # Update the name of the chat window
        chat_window.name = new_name
        session.commit()

        return jsonify({"message": "Chat window renamed successfully", "name": chat_window.name}), 200

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": f"Error renaming chat window: {str(e)}"}), 500
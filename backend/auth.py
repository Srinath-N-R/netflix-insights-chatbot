from flask import Blueprint, request, jsonify, redirect, url_for
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from tables import session, User, ChatWindow
import logging
from sqlalchemy import desc
from chat import create_new_chat_window

auth_bp = Blueprint('auth', __name__)



# Enable logging to see what’s happening during the request
logging.basicConfig(level=logging.INFO)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        # Get the JSON data sent by the frontend
        data = request.get_json()
        logging.info(f"Received registration data: {data['email']}")  # Logs incoming request data safely

        # Extract the user information from the request
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Check for missing fields
        if not all([username, email, password]):
            return jsonify(msg="Missing required fields"), 400

        # Check if the user already exists in the database
        existing_user = session.query(User).filter_by(email=email).first()
        if existing_user:
            logging.info(f"User {email} already exists")
            return jsonify(msg="User already exists"), 400

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        # If the user doesn't exist, create a new user
        new_user = User(username=username, email=email, password_hash=hashed_password)
        session.add(new_user)
        session.commit()

        logging.info(f"User {email} successfully registered")
        return jsonify(msg="Sign-up successful"), 200

    except SQLAlchemyError as e:
        session.rollback()  # Rollback in case of error
        logging.error(f"Database error during registration: {str(e)}")
        return jsonify(msg="An error occurred during registration"), 500

    except Exception as e:
        logging.error(f"Error during registration: {str(e)}")
        return jsonify(msg="An unexpected error occurred"), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not all([email, password]):
            return jsonify(msg="Missing email or password"), 400

        logging.info(f"Attempting login for {email}")

        # Find the user by email
        user = session.query(User).filter_by(email=email).first()

        # Check if the user exists and the password hash matches
        if user and check_password_hash(user.password_hash, password):
            # Create a JWT token
            access_token = create_access_token(identity=email)
            
            # Check for existing chat window for the user
            chat_window = session.query(ChatWindow).filter_by(user_id=user.user_id).order_by(desc(ChatWindow.created_at)).first()
            if not chat_window:
                chat_window_id = create_new_chat_window(user.user_id, chat_name="First Chat!")
            else:
                chat_window_id = chat_window.chat_window_id

            logging.info(f"User {email} successfully logged in with chat_window_id: {chat_window_id}")

            # Return both access token and chat_window_id
            return jsonify(access_token=access_token, user_id=user.user_id, chat_window_id=chat_window_id, msg="Login successful", username=user.username), 200
        else:
            logging.warning(f"Login failed for {email}")
            return jsonify(msg="Invalid email or password"), 401

    except SQLAlchemyError as e:
        session.rollback()  # Rollback in case of error
        logging.error(f"Database error during login: {str(e)}")
        return jsonify(msg="An error occurred during login"), 500

    except Exception as e:
        logging.error(f"Error during login: {str(e)}")
        return jsonify(msg="An unexpected error occurred during login"), 500

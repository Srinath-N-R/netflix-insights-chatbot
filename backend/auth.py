import os
from flask import Blueprint, request, jsonify, redirect, url_for, session, current_app
from flask_jwt_extended import create_access_token
from tables import session as db_session, User, ChatWindow
from chat import create_new_chat_window
import logging
from sqlalchemy import desc

auth_bp = Blueprint('auth', __name__)

# Enable logging to see what’s happening during the request
logging.basicConfig(level=logging.INFO)

# Google OAuth Login route
@auth_bp.route('/login/google')
def google_login():
    google = current_app.config['GOOGLE_OAUTH_CLIENT']
    redirect_uri = url_for('auth.google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

# Google OAuth callback route
@auth_bp.route('/google/callback')
def google_callback():
    try:
        google = current_app.config['GOOGLE_OAUTH_CLIENT']
        token = google.authorize_access_token()  # Exchange auth code for access token
        resp = google.get('https://www.googleapis.com/oauth2/v3/userinfo')  # Updated userinfo endpoint
        user_info = resp.json()
        email = user_info.get('email')
        name = user_info.get('name')

        if not email or not name:
            logging.error("Email or name not found in user info")
            return jsonify(msg="Failed to retrieve user information from Google"), 400

        # Check if user already exists in the database
        user = db_session.query(User).filter_by(email=email).first()

        if not user:
            logging.info(f"User {email} not found, creating new user")
            # Create a new user if not exists
            user = User(username=name, email=email, password_hash=None) 
            db_session.add(user)
            db_session.commit()
            logging.info(f"Created new user: {email}")
        else:
            logging.info(f"Existing user found: {email}")

        # Generate a JWT token
        access_token = create_access_token(identity=email)
        logging.info(f"Generated JWT token for user {email}")

        # Check for existing chat window for the user
        chat_window = db_session.query(ChatWindow).filter_by(user_id=user.user_id).order_by(desc(ChatWindow.created_at)).first()
        if not chat_window:
            chat_window_id = create_new_chat_window(user.user_id, chat_name="First Chat!")
            logging.info(f"Created new chat window for user {email}: {chat_window_id}")
        else:
            chat_window_id = chat_window.chat_window_id
            logging.info(f"Using existing chat window for user {email}: {chat_window_id}")

        # Store user session info
        session['profile'] = user_info
        session['token'] = token

        # Redirect to frontend with the JWT token in the query params
        FRONTEND_URL = os.environ.get('FRONTEND_URL')
        frontend_redirect_url = f"{FRONTEND_URL}/login?token={access_token}&chat_window_id={chat_window_id}&user_id={user.user_id}"
        return redirect(frontend_redirect_url)

    except Exception as e:
        logging.exception(f"Error during Google OAuth callback: {str(e)}")
        return jsonify(msg="An error occurred during Google login", error=str(e)), 500
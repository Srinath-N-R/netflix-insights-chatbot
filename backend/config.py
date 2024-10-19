import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv(override=True)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'a-very-secret-key')  # Default fallback if not provided
    GOOGLE_OAUTH_CLIENT_ID = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
    GOOGLE_OAUTH_CLIENT_SECRET = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-jwt-secret')  # Default fallback
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    EXTERNAL_DB_URL = os.getenv('EXTERNAL_DB_URL')
    CHAT_DB_URL = os.getenv('CHAT_DB_URL')

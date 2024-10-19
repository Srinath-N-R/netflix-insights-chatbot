import os
from flask import Flask
from flask_jwt_extended import JWTManager
from auth import auth_bp
from chat import chat_bp
from config import Config
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

# Apply ProxyFix to handle headers properly behind reverse proxies (like in Cloud Run)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Enable CORS dynamically based on environment variable for the frontend URL
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:8080')  # Default to localhost in dev
CORS(app, resources={r"/api/*": {"origins": FRONTEND_URL}})

# Set the secret keys and OAuth credentials from environment variables
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', Config.SECRET_KEY)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', Config.JWT_SECRET_KEY)
app.config['GOOGLE_OAUTH_CLIENT_ID'] = os.environ.get('GOOGLE_OAUTH_CLIENT_ID', Config.GOOGLE_OAUTH_CLIENT_ID)
app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET', Config.GOOGLE_OAUTH_CLIENT_SECRET)

# Initialize OAuth for Google login
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_OAUTH_CLIENT_ID'],
    client_secret=app.config['GOOGLE_OAUTH_CLIENT_SECRET'],
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# Initialize JWT
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(chat_bp, url_prefix='/api')

# Pass the `google` OAuth object to `auth.py`
app.config['GOOGLE_OAUTH_CLIENT'] = google

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from config import Config
from datetime import datetime

Base = declarative_base()


# User model
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(180), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=True)
    subscription_type = Column(String(50))
    account_creation_date = Column(DateTime, default=func.now())
    last_login = Column(DateTime)

    # Relationship with ChatWindow
    chat_windows = relationship('ChatWindow', back_populates='user')
    related_questions = relationship("RelatedQuestions", back_populates="user")


# Chat window model
class ChatWindow(Base):
    __tablename__ = 'chat_window'
    chat_window_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    created_at = Column(DateTime, default=func.now())
    name = Column(String(100), nullable=False)  # Add a name field with a max length of 100 characters
    deleted = Column(Boolean, default=False, nullable=False)  # Soft delete flag

    # Define the relationship to RelatedQuestions
    related_questions = relationship("RelatedQuestions", back_populates="chat_window")

    # Relationship back to the user
    user = relationship("User", back_populates="chat_windows")


# Chat history model
class ChatHistory(Base):
    __tablename__ = 'chat_history'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    chat_window_id = Column(Integer, ForeignKey('chat_window.chat_window_id'), nullable=False)
    user_message = Column(String)
    bot_response = Column(String)
    sender_role = Column(String)  # Either 'user' or 'bot'
    timestamp = Column(DateTime, default=datetime.utcnow)


class RelatedQuestions(Base):
    __tablename__ = 'related_questions'

    id = Column(Integer, primary_key=True)
    chat_window_id = Column(Integer, ForeignKey('chat_window.chat_window_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    question = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())

    chat_window = relationship("ChatWindow", back_populates="related_questions")
    user = relationship("User", back_populates="related_questions")


# Initialize database connection
engine = create_engine(Config.CHAT_DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Create tables if they don't exist
Base.metadata.create_all(engine)

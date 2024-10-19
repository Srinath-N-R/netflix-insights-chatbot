
# Netflix Insights Chatbot

This repository contains a chatbot application designed to provide insights into Netflix engagement trends for the year 2023. The system consists of a Flask backend and a React frontend, utilizing advanced AI models, RAG pipeline and text-to-sql to handle user queries about Netflix titles, technical specifications, and engagement trends.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [Backend](#backend)
- [Frontend](#frontend)
- [Docker Deployment](#docker-deployment)
- [API Endpoints](#api-endpoints)

## Features

- **GPT-4 powered Chat Interface**: The chatbot leverages GPT-4 models for natural conversation and data exploration.
- **Vector Search**: Uses LangChain's TimescaleVector for efficient similarity-based queries.
- **OAuth2 Authentication**: Supports Google login via OAuth2 for secure user access.
- **Rate Limiting**: Protects the API with rate limiting for a smoother experience.
- **SQL-based querying**: Provides insights into Netflix titles based on user queries.
- **Structured Responses**: Returns related questions to help users explore similar topics.

## Tech Stack

### Backend:
- Python (Flask)
- LangChain (TimescaleVector, ChatOpenAI)
- PostgreSQL (TimescaleDB for vector storage)
- JWT-based Authentication
- OAuth2 with Google
- SQLAlchemy ORM

### Frontend:
- ReactJS
- React Router
- Axios for HTTP requests
- JWT for authentication

## Setup Instructions

### Prerequisites

Make sure you have the following installed on your machine:

- Docker & Docker Compose
- Node.js (if running frontend locally)
- Python 3.9+

### Environment Variables

Create a `.env` file in the `backend` and `frontend` directories with the following variables:

#### Backend
```bash
SECRET_KEY=<your-secret-key>
JWT_SECRET_KEY=<your-jwt-secret-key>
GOOGLE_OAUTH_CLIENT_ID=<your-google-client-id>
GOOGLE_OAUTH_CLIENT_SECRET=<your-google-client-secret>
OPENAI_API_KEY=<your-openai-api-key>
EXTERNAL_DB_URL=<your-external-db-url>
CHAT_DB_URL=<your-chat-db-url>
FRONTEND_URL=<frontend-url>
```

#### Frontend
```bash
REACT_APP_BACKEND_URL=http://localhost:5001/api
```

### Backend

The backend is located in the `backend` folder and provides the agent setup for processing user input and retrieving insights from the database.

#### To Run Locally:

1. Install dependencies:
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

2. Start the Flask server:
    ```bash
    python app.py
    ```

### Frontend

The frontend is located in the `frontend` folder and provides a sleek chat interface for interacting with the chatbot.

#### To Run Locally:

1. Install dependencies:
    ```bash
    cd frontend
    npm install
    ```

2. Start the React development server:
    ```bash
    npm start
    ```

### Docker Deployment

You can easily deploy the entire system using Docker and Docker Compose.

1. Build and run the containers:
    ```bash
    docker-compose up --build
    ```

2. Access the frontend at `http://localhost:3000` and the backend at `http://localhost:5001/api`.

## API Endpoints

### Backend API Endpoints:

- **POST /api/chat**: Send a user message to the agent and receive a response.
- **GET /api/history**: Fetch the chat history of a user for a given chat window.
- **GET /api/chat-windows**: Retrieve all chat windows for a user.
- **POST /api/chat-windows**: Create a new chat window.

## License

This project is licensed under the MIT License.

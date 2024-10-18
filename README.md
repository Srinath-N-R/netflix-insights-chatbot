# Netflix Insights Chatbot

This project implements an interactive chatbot using RAG techniques to analyze Netflix and IMDb data. It leverages SQL agents and vector search for efficient querying, delivering insights on viewing trends and title performance.

## Features

- **Interactive Chat Interface:** Query Netflix insights in natural language.
- **Google OAuth:** Secure login using Google accounts.
- **Rate Limiting:** Prevent abuse with request rate limiting.
- **Scalable Architecture:** Containerized with Docker and orchestrated using Docker Compose.

## Technologies Used

- **Backend:** Flask, LangChain, OpenAI, PostgreSQL, Gunicorn
- **Frontend:** React, Axios
- **Infrastructure:** Docker, Nginx
- **Authentication:** Google OAuth (Flask-Dance)

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/netflix-insights-chatbot.git
   cd netflix-insights-chatbot

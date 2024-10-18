
# Netflix Insights Chatbot

A Netflix Insights Chatbot that provides information on Netflix engagement trends for movies and shows. This project consists of a **React frontend** and a **Flask backend** that processes queries, retrieves insights, and displays data.

## Project Structure

```
netflix-insights-chatbot/
├── backend/
│   ├── agent_helper.py
│   ├── agent_setup.py
│   ├── app.py
│   ├── auth.py
│   ├── chat.py
│   ├── config.py
│   ├── question_agent_setup.py
│   ├── tables.py
│   ├── requirements.txt
├── frontend/
│   ├── package.json
│   ├── src/
│   └── public/
├── docker-compose.yml
└── README.md
```

## Prerequisites

Make sure you have the following installed:
- [Python 3.x](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/en/download/)
- [Docker](https://docs.docker.com/get-docker/) (if using Docker for deployment)

## Setup

### 1. Backend (Flask)

1. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the environment variables by creating a `.env` file:
   ```
   JWT_SECRET_KEY=your_jwt_secret
   EXTERNAL_DB_URL=your_database_url
   ```

4. Run the backend:
   ```bash
   python app.py
   ```

The backend will start on port `5001`.

### 2. Frontend (React)

1. Navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up the environment variables by creating a `.env` file:
   ```
   REACT_APP_BACKEND_URL=http://localhost:5001
   ```

4. Run the frontend:
   ```bash
   npm start
   ```

The frontend will be available on port `3000`.

## Deployment

### A. Deploying the Frontend (Netlify or Vercel)

1. **Netlify**:
   - Connect your GitHub repo to Netlify.
   - Set the **build command** as `npm run build`.
   - Set the **publish directory** as `frontend/build`.
   - Add your environment variables (`REACT_APP_BACKEND_URL`) in the Netlify dashboard.

2. **Vercel**:
   - Connect your GitHub repo to Vercel.
   - Set the **build command** as `npm run build`.
   - Set the **output directory** as `frontend/build`.
   - Add your environment variables (`REACT_APP_BACKEND_URL`) in the Vercel dashboard.

### B. Deploying the Backend (Render or Heroku)

1. **Render**:
   - Connect your GitHub repo to Render.
   - Set the **build command** as `pip install -r requirements.txt`.
   - Set the **start command** as `python app.py`.
   - Add your environment variables (`JWT_SECRET_KEY`, `EXTERNAL_DB_URL`) in the Render dashboard.

2. **Heroku**:
   - Push your backend to Heroku using Git.
   - Set the **config variables** (`JWT_SECRET_KEY`, `EXTERNAL_DB_URL`) in the Heroku dashboard.

### C. Deploying with Docker

If you're deploying with Docker and Docker Compose:

1. Build the containers:
   ```bash
   docker-compose build
   ```

2. Run the containers:
   ```bash
   docker-compose up
   ```

Both the frontend and backend will be running as services.

## API Endpoints

### Authentication
- **POST** `/api/register`: User registration.
- **POST** `/api/login`: User login.

### Chat
- **POST** `/api/chat`: Submit a chat message.
- **GET** `/api/history`: Retrieve chat history.

## Environment Variables

Here are the necessary environment variables for the project:

| Variable                 | Description                                 |
|--------------------------|---------------------------------------------|
| `JWT_SECRET_KEY`          | Secret key for JWT authentication           |
| `EXTERNAL_DB_URL`         | URL for the external database               |
| `REACT_APP_BACKEND_URL`   | Backend API URL for React frontend requests |

Make sure these are set up in your environment or deployment platform.

## Technologies Used

- **Backend**: Flask, SQLAlchemy, JWT, OpenAI API
- **Frontend**: React, Axios
- **Database**: PostgreSQL (or any other compatible DB)
- **Deployment**: Netlify/Vercel (Frontend), Render/Heroku (Backend)

## Contributing

Feel free to submit issues or pull requests. Make sure to follow the contribution guidelines.

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

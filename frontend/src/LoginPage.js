import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import './LoginPage.css'; // Import the CSS for LoginPage

const LoginPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const navigate = useNavigate();

    const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5001/api';

    const handleLogin = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post(`${backendUrl}/login`, { email, password });
            if (response && response.data) {
                setSuccess('Login successful');
                setError('');
                localStorage.setItem('token', response.data.access_token);
                localStorage.setItem('user_id', response.data.user_id);  // Store user_id
                localStorage.setItem('chat_window_id', response.data.chat_window_id);  // Store chat_window_id
                setIsLoggedIn(true);
            } else {
                setError('Unexpected response from the server.');
                setSuccess('');
            }
        } catch (error) {
            if (error.response && error.response.data) {
                setError(error.response.data.msg || 'Login failed');
            } else {
                setError('An error occurred. Please try again.');
            }
            setSuccess('');
        }
    };
    

    useEffect(() => {
        if (isLoggedIn) {
            navigate('/chat');  // Redirect to the chat interface
        }
    }, [isLoggedIn, navigate]);

    return (
        <div className="login-page">
            <div className="background-animation"></div> {/* Animated Background */}
            <div className="login-container">
                <form onSubmit={handleLogin}>
                    <h2>Login</h2>
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    {error && <p className="error-message">{error}</p>}
                    {success && <p className="success-message">{success}</p>}
                    <button type="submit" className="login-btn">Login</button>
                    <p>Don't have an account? <Link to="/signup">Sign Up</Link></p>
                </form>
            </div>
        </div>
    );
};

export default LoginPage;
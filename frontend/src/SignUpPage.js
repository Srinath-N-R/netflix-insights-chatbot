import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './SignUpPage.css'; // Import the CSS for LoginPage

const SignUpPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [username, setUsername] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();

    const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5001/api';

    const handleSignUp = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post(`${backendUrl}/register`, {
                username,
                email,
                password,
            });

            if (response && response.data) {
                setSuccess('Sign-up successful');
                setError('');
                const loginResponse = await axios.post(`${backendUrl}/login`, { email, password });

                if (loginResponse && loginResponse.data) {
                    localStorage.setItem('token', loginResponse.data.access_token);
                    navigate('/chat');  // Redirect to chat
                } else {
                    setError('Sign-up succeeded, but auto-login failed. Please login manually.');
                }
            } else {
                setError('Unexpected response from the server.');
                setSuccess('');
            }
        } catch (error) {
            if (error.response && error.response.data) {
                setError(error.response.data.msg || 'Sign-up failed');
            } else {
                setError('An error occurred. Please try again.');
            }
            setSuccess('');
        }
    };

    return (
        <div className="signup-page">
            <div className="background-animation"></div> {/* Animated Background */}
            <div className="signup-container">
                <form onSubmit={handleSignUp}>
                    <h2>Sign Up</h2>
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
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
                    <button type="submit" className="signup-btn">Sign Up</button>
                    <p>Already have an account? <a href="/login">Login</a></p>
                </form>
            </div>
        </div>
    );
};

export default SignUpPage;
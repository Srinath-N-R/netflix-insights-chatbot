import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './LoginPage.css'; // Import the CSS for LoginPage

const LoginPage = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5001/api';

    // Handle Google Login Redirect
    const handleGoogleLogin = async () => {
        window.location.href = `${backendUrl}/login/google`;  // Redirect to Google OAuth login
    };

    // Handle extracting the token from URL params after Google OAuth login
    useEffect(() => {
        const queryParams = new URLSearchParams(location.search);
        const token = queryParams.get('token');
        const chatWindowId = queryParams.get('chat_window_id');
        const userId = queryParams.get('user_id');
    
        // Store in localStorage if all parameters exist
        if (token && chatWindowId && userId) {
            localStorage.setItem('token', token);
            localStorage.setItem('chat_window_id', chatWindowId);
            localStorage.setItem('user_id', userId);

            // After storing token and IDs, redirect to chat page
            navigate('/chat');
        } else {
            console.log("Missing parameters, token, chat_window_id, or user_id not found in URL.");
        }
    }, [location.search, navigate]);

    // Typing animation effect
    useEffect(() => {
        const text = "Ask me about Netflix Titles, 2023!";
        let index = 0;
        const typingElement = document.querySelector('.typing-text');
        const type = () => {
            if (index < text.length) {
                typingElement.innerHTML += text.charAt(index);
                index++;
                setTimeout(type, 100); // Adjust typing speed here
            }
        };
        type();
    }, []);

    return (
        <div className="login-page">
            <div className="background-animation"></div> {/* Animated Background */}
            <div className="login-container">
                <div className="typing-container">
                    <h1 className="typing-text"></h1> {/* Typing animation here */}
                </div>
                <div className="login-content">
                    {/* Google Login Button */}
                    <button className="google-login-btn" onClick={handleGoogleLogin}>
                        <img src="/images/google-logo.png" alt="Google Logo" />
                        Login with Google
                    </button>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;
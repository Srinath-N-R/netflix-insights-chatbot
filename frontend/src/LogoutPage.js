import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const LogoutPage = () => {
    const navigate = useNavigate();

    useEffect(() => {
        // Clear the token from localStorage
        localStorage.removeItem('token');

        // Redirect the user to the login page after clearing token
        navigate('/login');
    }, [navigate]);

    return (
        <div className="logout-container">
            <p>Logging out...</p>
        </div>
    );
};

export default LogoutPage;
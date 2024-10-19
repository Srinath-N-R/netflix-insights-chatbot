import React, { useEffect } from 'react';
import { Navigate, useLocation, useNavigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
    const token = localStorage.getItem('token');  // Check for the token in localStorage
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        if (!token) {
            // Replace the current history entry so the user can't navigate back to the protected route
            navigate('/login', { replace: true });
        }
    }, [token, navigate]);

    if (!token) {
        // If token is not found, prevent the protected content from rendering
        return <Navigate to="/login" replace />;
    }

    // If token exists, render the protected content
    return children;
};

export default ProtectedRoute;
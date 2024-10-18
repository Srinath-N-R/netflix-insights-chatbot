import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
    const token = localStorage.getItem('token'); // Check for the token in localStorage

    if (!token) {
        // If token is not found, redirect to the login page
        return <Navigate to="/login" />;
    }

    // If token is found, render the child components (protected content)
    return children;
};

export default ProtectedRoute;
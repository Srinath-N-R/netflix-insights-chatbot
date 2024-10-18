import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SignUpPage from './SignUpPage';
import LoginPage from './LoginPage';
import ChatInterface from './ChatInterface';
import ProtectedRoute from './ProtectedRoute'; // Import the ProtectedRoute component

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<LoginPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/signup" element={<SignUpPage />} />
                
                {/* Protect the /chat route */}
                <Route 
                    path="/chat" 
                    element={
                        <ProtectedRoute>
                            <ChatInterface />
                        </ProtectedRoute>
                    } 
                />
            </Routes>
        </Router>
    );
}

export default App;
import React, { useEffect, useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './ChatInterface.css'; // External CSS for better styling
import ChatWindowList from './ChatWindowList'; // Import the ChatWindowList component
import './ChatWindowList.css'; // Import the CSS for ChatWindowList

const ChatInterface = () => {
    const [messages, setMessages] = useState([]);
    const [relatedQuestions, setRelatedQuestions] = useState([]); // State for related questions
    const [input, setInput] = useState('');
    const [typingMessage, setTypingMessage] = useState('');
    const messageListRef = useRef(null);
    const username = localStorage.getItem('username') || 'You';
    const navigate = useNavigate();

    // State for Selected Chat Window
    const [selectedChatWindowId, setSelectedChatWindowId] = useState(localStorage.getItem('chat_window_id'));

    // Fetch related questions function (moved outside useEffect)
    const fetchRelatedQuestions = async (chatWindowId) => {
        try {
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/chat-windows/${chatWindowId}/related-questions`, {
            
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            });
            if (response.data && Array.isArray(response.data)) {
                setRelatedQuestions(response.data.map(q => q.question));
            } else {
                setRelatedQuestions([]);
            }
        } catch (error) {
            console.error('Error fetching related questions:', error.response ? error.response.data : error.message);
            setRelatedQuestions([]); // Clear related questions on error
        }
    };

    // Fetch chat history and related questions when selectedChatWindowId changes
    useEffect(() => {
        const fetchChatHistory = async () => {
            const chatWindowId = selectedChatWindowId;
            const userId = localStorage.getItem('user_id');

            if (!chatWindowId || !userId) {
                console.error('chat_window_id or user_id is missing');
                setMessages([]);
                return;
            }

            try {
                const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/history`, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`
                    },
                    params: {
                        chat_window_id: chatWindowId
                    }
                });
                if (response.data && Array.isArray(response.data)) {
                    setMessages(response.data);
                } else {
                    setMessages([]);
                }
            } catch (error) {
                console.error('Error fetching chat history:', error.response ? error.response.data : error.message);
                setMessages([]);
            }
        };

        if (selectedChatWindowId) {
            // Clear previous messages and related questions
            setMessages([]);
            setRelatedQuestions([]);

            // Fetch new chat history and related questions
            fetchChatHistory();
            fetchRelatedQuestions(selectedChatWindowId);
        }
    }, [selectedChatWindowId]);

    // Simulate typing stages for bot responses
    const simulateTypingStages = async (responseText) => {
        const stages = [
            "Analyzing engagement trends...",
            "Fetching streaming data...",
            "Crunching numbers...",
            "Generating insights..."
        ];

        for (let stage of stages) {
            setTypingMessage(stage);
            await new Promise(resolve => setTimeout(resolve, 500));
        }

        setTypingMessage('');
        setMessages((prevMessages) => [
            ...prevMessages,
            {
                message: responseText,
                sender_role: 'bot',
                timestamp: new Date().toISOString(),
            }
        ]);
    };

    // Handle message sending
    const handleSend = async () => {
        if (!input) return;

        const newMessage = {
            message: input,
            sender_role: 'user',
            timestamp: new Date().toISOString()
        };
        setMessages((prevMessages) => [...prevMessages, newMessage]);
        setInput('');
        setTypingMessage("Bot is thinking...");

        try {
            const chatWindowId = selectedChatWindowId;
            const userId = localStorage.getItem('user_id');

            if (!chatWindowId || !userId) {
                console.error('chat_window_id or user_id is missing');
                setMessages((prevMessages) => [
                    ...prevMessages,
                    {
                        message: 'Error: Missing chat window or user information.',
                        sender_role: 'bot',
                        timestamp: new Date().toISOString()
                    }
                ]);
                return;
            }

            const response = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/chat`, {
                message: input,
                chat_window_id: chatWindowId,
                user_id: userId
            }, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            });

            if (response.data && response.data.response) {
                simulateTypingStages(response.data.response);
                setRelatedQuestions(response.data.related_questions || []); // Update related questions
            }
        } catch (error) {
            console.error('Error sending message:', error.response ? error.response.data : error.message);
            setMessages((prevMessages) => [
                ...prevMessages,
                {
                    message: 'Error in response. Please try again.',
                    sender_role: 'bot',
                    timestamp: new Date().toISOString()
                }
            ]);
            setTypingMessage('');
        }
    };

    // Handle Chat Window Selection
    const handleSelectChat = (chatWindowId) => {
        setSelectedChatWindowId(chatWindowId);
        localStorage.setItem('chat_window_id', chatWindowId);
    };

    // Handle logout functionality
    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('chat_window_id');
        navigate('/login');

        window.history.pushState(null, "", window.location.href);
        window.history.go(1);
    };

    // Format the date for display
    const formatDate = (timestamp) => {
        const date = new Date(timestamp);
        return date.toLocaleDateString([], { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' });
    };

    // Check if two messages are on the same day
    const isSameDay = (timestamp1, timestamp2) => {
        const date1 = new Date(timestamp1);
        const date2 = new Date(timestamp2);
        return date1.toDateString() === date2.toDateString();
    };

    // Render structured content for messages like movie lists
    const formatStructuredContent = (message) => {
        const parts = message.split('\n').map((line, index) => (
            <p key={index} className="structured-text">{line.replace(/\*\*/g, '')}</p>
        ));

        return <div className="structured-list">{parts}</div>;
    };

    return (
        <div className="chat-interface">
            {/* Floating Logout Button */}
            <button className="logout-btn" onClick={handleLogout}>Logout</button>

            <div className="chat-container">
                {/* Chat Window List Always Visible on the Left */}
                <div className="chat-window-list-container">
                    <ChatWindowList onSelectChat={handleSelectChat} selectedChatId={selectedChatWindowId} />
                </div>

                {/* Chat Content */}
                <div className="chat-content">
                    {/* Chatbot Header */}
                    <div className="chat-header">Ask me about Netflix Titles, 2023!</div>

                    {/* Message List */}
                    <div className="message-list" ref={messageListRef}>
                        {messages.map((msg, index) => {
                            const showDate = index === 0 || !isSameDay(messages[index - 1].timestamp, msg.timestamp);

                            return (
                                <React.Fragment key={index}>
                                    {showDate && (
                                        <div className="date-divider">
                                            {formatDate(msg.timestamp)}
                                        </div>
                                    )}

                                    <div className={`message ${msg.sender_role === 'user' ? 'user-message' : 'bot-message'}`}>
                                        <div className="message-content">
                                            {msg.sender_role === 'bot' && (
                                                <img src="/images/bot-icon.png" alt="Bot Icon" className="message-icon" />
                                            )}
                                            <div>{formatStructuredContent(msg.message)}</div>
                                        </div>
                                    </div>
                                </React.Fragment>
                            );
                        })}

                        {typingMessage && (
                            <div className="message bot-message">
                                <img src="/images/bot-icon.png" alt="Bot Icon" className="message-icon" />
                                {typingMessage}
                            </div>
                        )}
                    </div>

                    {/* Input Field */}
                    <div className="message-input-container">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                            placeholder="Type a message..."
                            className="message-input"
                        />
                        <button onClick={handleSend} disabled={!!typingMessage} className="send-button">
                            Send
                        </button>
                    </div>

                    {/* Quick Reply Buttons Based on Related Questions */}
                    <div className="quick-replies">
                        {relatedQuestions.length > 0 ? (
                            relatedQuestions.map((question, index) => (
                                <button
                                    key={index}
                                    className="quick-reply-button"
                                    onClick={() => setInput(question)}
                                >
                                    {question}
                                </button>
                            ))
                        ) : (
                            // Default quick reply buttons if no related questions are available
                            <>
                                <button className="quick-reply-button" onClick={() => setInput('Show me top Netflix titles')}>Show me top Netflix titles</button>
                                <button className="quick-reply-button" onClick={() => setInput('Explain engagement trends')}>Explain engagement trends</button>
                            </>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChatInterface;

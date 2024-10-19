import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './ChatWindowList.css';

const ChatWindowList = ({ onSelectChat, selectedChatId }) => {
    const [chatWindows, setChatWindows] = useState([]);
    const [newChatName, setNewChatName] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [renameId, setRenameId] = useState(null); // To track the renaming chat window
    const [renameValue, setRenameValue] = useState('');
    const [menuVisibleId, setMenuVisibleId] = useState(null); // To track which chat window's menu is visible

    // Fetch chat windows when the component mounts
    useEffect(() => {
        const fetchChatWindows = async () => {
            const token = localStorage.getItem('token');
            console.log("Token in localStorage:", token);  // Log to see if the token is fetched
    
            if (!token) {
                console.error("Token not found in localStorage");
                setError("Token is missing. Please log in again.");
                return;
            }
    
            try {
                const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/chat-windows`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                    params: { limit: 20 },
                });
    
                if (response && response.data) {
                    setChatWindows(response.data);
                }
            } catch (error) {
                console.error("Error fetching chat windows:", error);
                setError("Error fetching chat windows");
            }
        };
        fetchChatWindows();
    }, []);

    const createNewChatWindow = async () => {
        if (!newChatName.trim()) {
            return alert('Please provide a name for the new chat window.');
        }

        setLoading(true);

        try {
            const response = await axios.post(
                `${process.env.REACT_APP_BACKEND_URL}/chat-windows`,
                {
                    name: newChatName,
                },
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`,
                    },
                }
            );

            if (response.data) {
                setChatWindows([response.data, ...chatWindows.slice(0, 19)]);
                setNewChatName('');

                // Select the new chat window
                onSelectChat(response.data.id);
            }
        } catch (error) {
            setError('Error creating new chat window');
            console.error(
                'Error creating new chat window:',
                error.response ? error.response.data : error.message
            );
        } finally {
            setLoading(false);
        }
    };

    const renameChatWindow = async (chatId) => {
        if (!renameValue.trim()) {
            return alert('Please provide a new name.');
        }

        setLoading(true);

        try {
            const response = await axios.put(
                `${process.env.REACT_APP_BACKEND_URL}/chat-windows/${chatId}`,
                {
                    name: renameValue,
                },
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`,
                    },
                }
            );

            if (response.data) {
                setChatWindows(
                    chatWindows.map((chat) =>
                        chat.id === chatId ? { ...chat, name: response.data.name } : chat
                    )
                );
                setRenameId(null);
                setRenameValue('');
            }
        } catch (error) {
            setError('Error renaming chat window');
            console.error(
                'Error renaming chat window:',
                error.response ? error.response.data : error.message
            );
        } finally {
            setLoading(false);
        }
    };

    const fetchChatWindows = async () => {
        try {
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/chat-windows`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            });
            setChatWindows(response.data);
        } catch (error) {
            setError('Error fetching chat windows');
            console.error(
                'Error fetching chat windows:',
                error.response ? error.response.data : error.message
            );
        }
    };


    const deleteChatWindow = async (chatId) => {
        setLoading(true);

        try {
            const response = await axios.delete(`${process.env.REACT_APP_BACKEND_URL}/chat-windows/${chatId}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            });

            // Re-fetch the updated chat windows from the server
            await fetchChatWindows(); // Make sure you have this function fetching the data
        } catch (error) {
            setError('Error deleting chat window');
            console.error(
                'Error deleting chat window:',
                error.response ? error.response.data : error.message
            );
        } finally {
            setLoading(false);
        }
    };

    // Handle the escape key press to close the menu
    useEffect(() => {
        const handleEscape = (event) => {
            if (event.key === 'Escape') {
                setMenuVisibleId(null); // Close the menu when Escape is pressed
                setRenameId(null); // Close rename input if open
            }
        };

        document.addEventListener('keydown', handleEscape);

        return () => {
            document.removeEventListener('keydown', handleEscape); // Clean up the event listener
        };
    }, []);

    // Close the menu when clicking outside
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (!event.target.closest('.chat-window-item')) {
                setMenuVisibleId(null);
                setRenameId(null);
            }
        };

        document.addEventListener('click', handleClickOutside);

        return () => {
            document.removeEventListener('click', handleClickOutside);
        };
    }, []);

    return (
        <div className="chat-window-list">
            {error && <div className="error-message">{error}</div>}

            <div className="create-chat">
                <input
                    type="text"
                    placeholder="New chat name"
                    value={newChatName}
                    onChange={(e) => setNewChatName(e.target.value)}
                    className="new-chat-input"
                    disabled={loading}
                />
                <button
                    onClick={createNewChatWindow}
                    className="create-chat-button"
                    disabled={loading}
                >
                    {loading ? 'Creating...' : 'Create'}
                </button>
            </div>

            {loading && <div className="loading-message">Loading...</div>}

            {chatWindows.map((chat) => (
                <div
                    key={chat.id}
                    className={`chat-window-item ${
                        chat.id === selectedChatId ? 'active' : ''
                    } ${menuVisibleId === chat.id ? 'menu-open' : ''}`}
                >
                    <div
                        className="chat-window-content"
                        onClick={() => onSelectChat(chat.id)}
                    >
                        {renameId === chat.id ? (
                            <input
                                type="text"
                                value={renameValue}
                                onChange={(e) => setRenameValue(e.target.value)}
                                onBlur={() => {
                                    setRenameId(null);
                                    setRenameValue('');
                                }}
                                onKeyDown={(e) => {
                                    if (e.key === 'Enter') {
                                        renameChatWindow(chat.id);
                                    } else if (e.key === 'Escape') {
                                        setRenameId(null);
                                        setRenameValue('');
                                    }
                                }}
                                autoFocus
                                className="rename-input"
                            />
                        ) : (
                            <span>{chat.name}</span>
                        )}
                    </div>

                    <button
                        className="menu-button"
                        onClick={(e) => {
                            e.stopPropagation(); // Prevent triggering onSelectChat
                            setMenuVisibleId(
                                menuVisibleId === chat.id ? null : chat.id
                            );
                            setRenameId(null); // Close rename input if any other menu is opened
                        }}
                    >
                        &#x2022;&#x2022;&#x2022; {/* Three dots */}
                    </button>

                    {/* The dropdown menu for rename and delete */}
                    {menuVisibleId === chat.id && (
                        <div className="dropdown-menu visible">
                            <div
                                className="dropdown-item"
                                onClick={(e) => {
                                    e.stopPropagation();
                                    setRenameId(chat.id);
                                    setRenameValue(chat.name);
                                    setMenuVisibleId(null);
                                }}
                            >
                                Rename
                            </div>
                            <div
                                className="dropdown-item"
                                onClick={(e) => {
                                    e.stopPropagation();
                                    deleteChatWindow(chat.id);
                                    setMenuVisibleId(null);
                                }}
                            >
                                Delete
                            </div>
                        </div>
                    )}
                </div>
            ))}
        </div>
    );
};

export default ChatWindowList;

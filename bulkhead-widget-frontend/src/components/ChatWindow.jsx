// Main Container
import React, { useState } from 'react';
import MessageList from './MessageList';
import InputArea from './InputArea';
import useChatFlow from '../hooks/useChatFlow';

const ChatWindow = () => {
    const [isOpen, setIsOpen] = useState(false);
    const { messages, handleUserInput } = useChatFlow();

    return (
        <div className="bh-bot-container">
            {isOpen && (
                <div className="bh-bot-window">
                    <div className="bh-bot-header">
                        Marine Construction Assistant
                    </div>
                    <MessageList messages={messages} />
                    <InputArea onSendMessage={handleUserInput} />
                </div>
            )}

            <button
                className="bh-bot-toggle-btn"
                onClick={() => setIsOpen(!isOpen)}
            >
                {isOpen ? 'Close Chat' : 'Open Chat'}
            </button>
        </div>
    );
};

export default ChatWindow;
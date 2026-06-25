// Render the conversation
import React, { useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';

const MessageList = ({ messages }) => {
    const endOfMessagesRef = useRef(null);

    // Auto-scroll to the bottom when a new message arrives
    useEffect(() => {
        endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    return (
        <div style={{ flex: 1, padding: '15px', overflowY: 'auto', backgroundColor: '#f8f9fa' }}>
            {messages.map((msg, index) => (
                <MessageBubble key={index} text={msg.text} sender={msg.sender} />
            ))}
            <div ref={endOfMessagesRef} />
        </div>
    );
};

export default MessageList;
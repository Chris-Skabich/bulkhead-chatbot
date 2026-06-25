// Individual user/bot messages
import React from 'react';

const MessageBubble = ({ text, sender }) => {
    const isBot = sender === 'bot';

    const containerStyle = {
        display: 'flex',
        justifyContent: isBot ? 'flex-start' : 'flex-end',
        width: '100%',
        marginBottom: '10px'
    };

    const bubbleStyle = {
        maxWidth: '75%',
        padding: '10px 14px',
        borderRadius: '16px',
        fontSize: '14px',
        lineHeight: '1.4',
        backgroundColor: isBot ? '#e9ecef' : '#0056b3',
        color: isBot ? '#212529' : 'white',
        borderBottomLeftRadius: isBot ? '4px' : '16px',
        borderBottomRightRadius: isBot ? '16px' : '4px',
    };

    return (
        <div style={containerStyle}>
            <div style={bubbleStyle}>{text}</div>
        </div>
    );
};

export default MessageBubble;
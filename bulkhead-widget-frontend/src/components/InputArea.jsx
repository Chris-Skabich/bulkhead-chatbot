// Text input and send button
import React, { useState } from 'react';

const InputArea = ({ onSendMessage }) => {
    const [inputValue, setInputValue] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (inputValue.trim() === '') return;

        onSendMessage(inputValue);
        setInputValue('');
    };

    return (
        <form
            onSubmit={handleSubmit}
            style={{ display: 'flex', padding: '12px', borderTop: '1px solid #dee2e6', backgroundColor: 'white' }}
        >
            <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Type your reply..."
                style={{ flex: 1, padding: '10px', borderRadius: '20px', border: '1px solid #ced4da', outline: 'none' }}
            />
            <button
                type="submit"
                style={{ marginLeft: '8px', padding: '10px 18px', backgroundColor: '#0056b3', color: 'white', border: 'none', borderRadius: '20px', cursor: 'pointer', fontWeight: 'bold' }}
            >
                Send
            </button>
        </form>
    );
};

export default InputArea;
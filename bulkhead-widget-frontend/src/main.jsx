// Entry point: Mounts React to a specific DOM ID
import React from 'react';
import ReactDOM from 'react-dom/client';
import ChatWindow from './components/ChatWindow';
import './index.css';

// Find the host element on the client's website
const rootElement = document.getElementById('bulkhead-bot-root');

if (rootElement) {
    ReactDOM.createRoot(rootElement).render(
        <React.StrictMode>
            <ChatWindow />
        </React.StrictMode>
    );
} else {
    console.error('Bulkhead Bot Error: Target container #bulkhead-bot-root not found.');
}
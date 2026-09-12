// Entry point: Mounts React to a specific DOM ID
import React from 'react';
import ReactDOM from 'react-dom/client';
import Dashboard from './Dashboard'; // Import the Dashboard
// import ChatWindow from './components/ChatWindow'; // Temporarily commented out
import './index.css';

// Find the host element on the client's website (or your local index.html)
const rootElement = document.getElementById('bulkhead-bot-root');

if (rootElement) {
    ReactDOM.createRoot(rootElement).render(
        <React.StrictMode>
            <Dashboard />
        </React.StrictMode>
    );
} else {
    console.error('Bulkhead Bot Error: Target container #bulkhead-bot-root not found.');
}
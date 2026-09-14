import React from 'react';
import ReactDOM from 'react-dom/client';
import Dashboard from './Dashboard'; 
import BulkheadWidget from './BulkheadWidget'; // We will create this file next
import './index.css';

const rootElement = document.getElementById('bulkhead-bot-root');

if (rootElement) {
    // Check if the HTML element has an API key attached to it
    const apiKey = rootElement.getAttribute('data-api-key');

    if (apiKey) {
        // Client's website (Render the Chatbot Widget)
        ReactDOM.createRoot(rootElement).render(
            <React.StrictMode>
                <BulkheadWidget apiKey={apiKey} />
            </React.StrictMode>
        );
    } else {
        // Your internal admin site (Render the Dashboard)
        ReactDOM.createRoot(rootElement).render(
            <React.StrictMode>
                <Dashboard />
            </React.StrictMode>
        );
    }
} else {
    console.error('Bulkhead Bot Error: Target container #bulkhead-bot-root not found.');
}
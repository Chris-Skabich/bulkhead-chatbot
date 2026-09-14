import React, { useState, useEffect } from 'react';
import ChatWindow from './components/ChatWindow'; // Assuming this is where your actual chat UI lives!

const BulkheadWidget = ({ apiKey }) => {
    const [config, setConfig] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const verifyWidget = async () => {
            try {
                const response = await fetch(`http://localhost:8000/widget/config?api_key=${apiKey}`);
                
                if (response.ok) {
                    const data = await response.json();
                    setConfig(data);
                } else {
                    console.error("Bulkhead Bot: Invalid API Key.");
                    setConfig({ is_active: false });
                }
            } catch (error) {
                console.error("Bulkhead Bot: Network Error.");
                setConfig({ is_active: false });
            }
            setLoading(false);
        };

        if (apiKey) {
            verifyWidget();
        } else {
            setLoading(false);
        }
    }, [apiKey]);

    if (loading) return null; // Or return a small loading spinner

    // If deactivated or key is invalid, render nothing
    if (!config || !config.is_active) return null; 

    // Otherwise, render the active chat interface!
    // We pass company_id down so the ChatWindow knows where to save the leads
    return (
        <div className="bulkhead-bot-container">
            <ChatWindow companyId={config.company_id} companyName={config.company_name} />
        </div>
    );
};

export default BulkheadWidget;
import { useState } from 'react';

const useChatFlow = () => {
    const [messages, setMessages] = useState([
        { sender: 'bot', text: 'Hi! I can help you get a quote for your bulkhead project. What is your name?' }
    ]);
    const [step, setStep] = useState(1);
    const [leadData, setLeadData] = useState({});

    const handleUserInput = (inputText) => {
        // If the chat is done (step 5), ignore any new typing
        if (step > 4) return;

        const newMessages = [...messages, { sender: 'user', text: inputText }];
        setMessages(newMessages);

        setTimeout(() => {
            let botReply = '';

            switch (step) {
                case 1:
                    setLeadData((prev) => ({ ...prev, name: inputText }));
                    botReply = `Nice to meet you! What is the estimated length of the wall in linear feet?`;
                    setStep(2);
                    break;
                case 2:
                    // Match the exact 'linear_feet' key your Pydantic schema expects
                    setLeadData((prev) => ({ ...prev, linear_feet: parseInt(inputText) || 0 }));
                    botReply = `Got it. What material is currently there? (e.g., Wood, Vinyl, Concrete)`;
                    setStep(3);
                    break;
                case 3:
                    // Match the exact 'notes' key your Pydantic schema expects
                    setLeadData((prev) => ({ ...prev, notes: "Current material: " + inputText }));
                    botReply = `Thanks! Lastly, please provide your phone number so our team can call you tomorrow.`;
                    setStep(4);
                    break;
                default:
                    const finalLeadData = { ...leadData, phone: inputText };
                    setLeadData(finalLeadData);
                    botReply = `Thank you! We have received your information and will be in touch shortly.`;
                    
                    // Advance to step 5 so the switch statement never fires 'default' again
                    setStep(5);
                    
                    const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
                    
                    fetch(`${apiUrl}/leads`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(finalLeadData),
                    })
                    .then(response => response.json())
                    .then(data => console.log("Lead successfully saved to DB:", data))
                    .catch((error) => console.error("Error saving lead:", error));
            }

            setMessages([...newMessages, { sender: 'bot', text: botReply }]);
        }, 600);
    };

    return { messages, handleUserInput };
};

export default useChatFlow;

import { useState } from 'react';

const useChatFlow = () => {
    const [messages, setMessages] = useState([
        { sender: 'bot', text: 'Hi! I can help you get a quote for your bulkhead project. What is your name?' }
    ]);
    const [step, setStep] = useState(1);
    const [leadData, setLeadData] = useState({});

    const handleUserInput = (inputText) => {
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
                    // Changed 'size' to 'linear_feet' to match backend schema. 
                    // parseInt ensures it sends as a number, not a string!
                    setLeadData((prev) => ({ ...prev, linear_feet: parseInt(inputText) || 0 }));
                    botReply = `Got it. What material is currently there? (e.g., Wood, Vinyl, Concrete)`;
                    setStep(3);
                    break;
                case 3:
                    // Changed 'material' to 'notes' to match backend schema
                    setLeadData((prev) => ({ ...prev, notes: "Current material: " + inputText }));
                    botReply = `Thanks! Lastly, please provide your phone number so our team can call you tomorrow.`;
                    setStep(4);
                    break;
                default:
                    // Capture the phone number
                    const finalLeadData = { ...leadData, phone: inputText };
                    setLeadData(finalLeadData);
                    botReply = `Thank you! We have received your information and will be in touch shortly.`;
                    
                    // Send the data to your live FastAPI backend
                    fetch('http://localhost:8000/leads', {
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

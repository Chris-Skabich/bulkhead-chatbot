// Manages conversation state and transitions
import { useState } from 'react';

const useChatFlow = () => {
    const [messages, setMessages] = useState([
        { sender: 'bot', text: 'Hi! I can help you get a quote for your bulkhead project. What is your name?' }
    ]);
    const [step, setStep] = useState(1);
    const [leadData, setLeadData] = useState({}); // We will use leadData and setLeadData when we set up the database in backend

    const handleUserInput = (inputText) => {
        // Immediately show the user's message in the chat
        const newMessages = [...messages, { sender: 'user', text: inputText }];
        setMessages(newMessages);

        // Determine the bot's next reply with a slight delay for realism
        setTimeout(() => {
            let botReply = '';

            // This switch statement is temporary and will go through changes
            switch (step) {
                case 1:
                    setLeadData((prev) => ({ ...prev, name: inputText }));
                    botReply = `Nice to meet you! What is the estimated length of the wall in linear feet?`;
                    setStep(2);
                    break;
                case 2:
                    setLeadData((prev) => ({ ...prev, size: inputText }));
                    botReply = `Got it. What material is currently there? (e.g., Wood, Vinyl, Concrete)`;
                    setStep(3);
                    break;
                case 3:
                    setLeadData((prev) => ({ ...prev, material: inputText }));
                    botReply = `Thanks! Lastly, please provide your phone number so our team can call you tomorrow.`;
                    setStep(4);
                    break;
                default:
                    botReply = `Thank you! We have received your information and will be in touch shortly.`;
                // In the future: call api.submitLead(leadData) here
            }

            setMessages([...newMessages, { sender: 'bot', text: botReply }]);
        }, 600);
    };

    return { messages, handleUserInput };
};

export default useChatFlow;
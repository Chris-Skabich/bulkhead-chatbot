import { useState } from 'react';
import { submitLead } from '../services/api';

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
                    setMessages([...newMessages, { sender: 'bot', text: botReply }]);
                    break;
                
                case 2:
                    setLeadData((prev) => ({ ...prev, linear_feet: parseInt(inputText) || 0 }));
                    botReply = `Got it. What material is currently there? (e.g., Wood, Vinyl, Concrete)`;
                    setStep(3);
                    setMessages([...newMessages, { sender: 'bot', text: botReply }]);
                    break;
                
                case 3:
                    setLeadData((prev) => ({ ...prev, notes: "Current material: " + inputText }));
                    botReply = `Thanks! Lastly, please provide your phone number so our team can call you tomorrow.`;
                    setStep(4);
                    setMessages([...newMessages, { sender: 'bot', text: botReply }]);
                    break;
                
                case 4:
                    const finalLeadData = { ...leadData, phone: inputText };
                    setLeadData(finalLeadData);
                    
                    // Advance to step 5 to lock the chat
                    setStep(5);
                    
                    // Show a temporary processing state
                    setMessages([...newMessages, { sender: 'bot', text: 'Thank you! Submitting your information...' }]);
                    
                    // Call the dedicated API service
                    submitLead(finalLeadData).then((data) => {
                        if (!data || data.success === false) {
                            // Remove the loading message and show error
                            setMessages((prev) => [
                                ...prev.filter(m => m.text !== 'Thank you! Submitting your information...'),
                                { sender: 'bot', text: 'Oops! We had trouble saving your info. Please call us directly.' }
                            ]);
                        } else {
                            // Remove the loading message and show success
                            setMessages((prev) => [
                                ...prev.filter(m => m.text !== 'Thank you! Submitting your information...'),
                                { sender: 'bot', text: 'Success! Your quote request has been received. Our team will call you tomorrow.' }
                            ]);
                        }
                    });
                    break;
                
                default:
                    break;
            }
        }, 600);
    };

    return { messages, handleUserInput };
};

export default useChatFlow;
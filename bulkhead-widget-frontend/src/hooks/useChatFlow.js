import { useState } from 'react';
import { submitLead } from '../services/api';

const useChatFlow = (companyId) => {
    const [messages, setMessages] = useState([
        { sender: 'bot', text: 'Hi! I can help you get a quote for your bulkhead project. What is your name?' }
    ]);
    const [step, setStep] = useState(1);
    const [leadData, setLeadData] = useState({});

    const handleUserInput = (inputText) => {
        // Stop accepting input if the chat is finished
        if (step > 6) return;

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
                    botReply = `Great! What type of project is this? (e.g., Bulkhead, Dock, Repair)`;
                    setStep(3);
                    setMessages([...newMessages, { sender: 'bot', text: botReply }]);
                    break;

                case 3:
                    setLeadData((prev) => ({ ...prev, project_type: inputText }));
                    botReply = `Got it. What kind of material are you considering? (e.g., Vinyl, Wood, Steel)`;
                    setStep(4);
                    setMessages([...newMessages, { sender: 'bot', text: botReply }]);
                    break;

                case 4:
                    setLeadData((prev) => ({ ...prev, notes: "Material: " + inputText }));
                    botReply = `When are you hoping to complete this project?`;
                    setStep(5);
                    setMessages([...newMessages, { sender: 'bot', text: botReply }]);
                    break;

                case 5:
                    setLeadData((prev) => ({ ...prev, timeline: inputText }));
                    botReply = `Thanks! Lastly, please provide your phone number so our team can call you tomorrow.`;
                    setStep(6);
                    setMessages([...newMessages, { sender: 'bot', text: botReply }]);
                    break;

                case 6:
                    const finalLeadData = { 
                        ...leadData, 
                        phone: inputText,
                        company_id: companyId 
                    };
                    
                    setLeadData(finalLeadData);
                    setStep(7); // Temporarily lock input while submitting

                    setMessages([...newMessages, { sender: 'bot', text: 'Thank you! Submitting your information...' }]);

                    submitLead(finalLeadData).then((data) => {
                        // Remove the loading message
                        setMessages((prev) => prev.filter(m => m.text !== 'Thank you! Submitting your information...'));

                        if (data && data.isRateLimited) {
                            // Rate Limit Hit
                            setMessages((prev) => [
                                ...prev,
                                { sender: 'bot', text: 'You are submitting requests too quickly. Please wait a few seconds and try again.' }
                            ]);
                            // Reset step to 6 so they can try sending their phone number again
                            setStep(6); 
                            
                        } else if (!data || data.success === false) {
                            // Server Error
                            setMessages((prev) => [
                                ...prev,
                                { sender: 'bot', text: 'Oops! We had trouble saving your info. Please call us directly.' }
                            ]);
                        } else {
                            // Success
                            setMessages((prev) => [
                                ...prev,
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
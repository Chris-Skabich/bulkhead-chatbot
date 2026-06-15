// Calls to FastAPI backend
export const submitLead = async (leadData) => {
    try {
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

        const response = await fetch(`${apiUrl}/api/leads`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(leadData),
        });

        if (!response.ok) {
            throw new Error('Failed to submit lead data');
        }

        return await response.json();
    } catch (error) {
        console.error('Error submitting lead:', error);
        return { success: false, error: error.message };
    }
};
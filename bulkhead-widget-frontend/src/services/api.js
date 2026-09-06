const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const submitLead = async (leadData) => {
    // 1. Combine the React data with your required company_id
    const fullPayload = {
        ...leadData,
        company_id: 1 // Change this to your actual company ID
    };

    console.log("SENDING TO FASTAPI:", fullPayload); // This will prove it works!

    try {
        const response = await fetch("http://localhost:8000/leads", { // Update to your actual API URL
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(fullPayload) // Now sending ALL fields!
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return { success: true, data };
    } catch (error) {
        console.error("Error submitting lead:", error);
        return { success: false, error: error.message };
    }
};
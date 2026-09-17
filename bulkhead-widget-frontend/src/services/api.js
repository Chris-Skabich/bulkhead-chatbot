export const submitLead = async (leadData) => {
    try {
        const response = await fetch("http://localhost:8000/leads/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(leadData)
        });

        // Check specifically for the Rate Limit status
        if (response.status === 429) {
            return { success: false, isRateLimited: true };
        }

        // Check for other server errors
        if (!response.ok) {
            return { success: false, isRateLimited: false };
        }

        // Success!
        const data = await response.json();
        return { success: true, data };
        
    } catch (error) {
        console.error("Network error:", error);
        return { success: false, isRateLimited: false };
    }
};
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const submitLead = async (leadData) => {
  try {
    // 1. Format the payload to strictly match FastAPI's LeadCreate schema
    const payload = {
      company_id: 1, // Make sure Company ID 1 actually exists in your database!
      name: leadData.name || "Unknown",
      phone: leadData.phone || "",
      // Fallback values for required fields the bot didn't ask for:
      email: "no-email-provided@example.com", 
      timeline: "Not specified",
      // Combine the specific bot answers into a descriptive string
      project_description: `Wall length: ${leadData.linear_feet || 0} ft. ${leadData.notes || ""}`,
    };

    console.log("Sending payload to FastAPI:", payload); // Look at this in your browser console!

    const response = await fetch(`${API_URL}/leads`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      // If FastAPI hates the data shape, this throws the error
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error submitting lead to Bulkhead API:", error);
    return null;
  }
};
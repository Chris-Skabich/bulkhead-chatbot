// Logic to parse user input and convert to linear ft
// Parses input
export const extractLinearFeet = (inputString) => {
    if (!inputString) return null;

    // Strips out all non-numeric characters
    const numericString = inputString.replace(/[^0-9]/g, '');

    const parsedValue = parseInt(numericString, 10);
    return isNaN(parsedValue) ? null : parsedValue;
};
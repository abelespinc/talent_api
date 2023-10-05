// Truncate the text adding an ellipsis if the text is longer than the max length
export const truncateText = (text: string, maxLength = 30): string =>
    `${text.substring(0, maxLength)}${text.length > maxLength ? '...' : ''}`

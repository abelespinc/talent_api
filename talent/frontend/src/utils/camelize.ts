export const camelize = (str: string) => {
    return str ? str.toLowerCase().replace(/[^a-zA-Z0-9]+(.)/g, (m, chr) => chr.toUpperCase()) : str
}

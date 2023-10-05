// https://stackoverflow.com/a/68047417
export function flattenObject(obj: Record<any, any>) {
    let res: Record<any, any> = {}

    for (const [key, value] of Object.entries(obj)) {
        if (typeof value === 'object') {
            res = { ...res, ...flattenObject(value) }
        } else {
            res[key] = value
        }
    }

    return res
}

export function prepareObjectForQuery(obj: Record<any, any>) {
    /**
     * Removes undefined, null, '' and NaN values from the object
     */
    return Object.fromEntries(Object.entries(obj).filter(([_, value]) => ![undefined, null, '', NaN].includes(value)))
}

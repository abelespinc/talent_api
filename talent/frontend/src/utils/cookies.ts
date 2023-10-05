function getDefaultCookieExpirationDate() {
    const now = new Date()
    now.setMonth(now.getMonth() + 6)
    return now
}

export function getCookiesAsObject() {
    return Object.fromEntries(document.cookie.split(';').map((cookie) => cookie.split('=').map((el) => el.trim())))
}

export function getCookie(cookieName: string) {
    return getCookiesAsObject()[cookieName]
}

export function setCookie(cookieName: string, value: string, expiration?: string, path = '/') {
    document.cookie = `${cookieName}=${value}; expires=${expiration || getDefaultCookieExpirationDate()}; path=${path};`
}

export function removeCookie(cookieName: string, path = '/') {
    document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=${path};`
}

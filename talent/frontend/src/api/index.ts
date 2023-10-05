import { defaults } from 'mande'

export function setApiAuthToken(authToken: string) {
    defaults.headers.Authorization = `Token ${authToken}`
}

export function removeApiAuthToken() {
    defaults.headers.Authorization = ''
}

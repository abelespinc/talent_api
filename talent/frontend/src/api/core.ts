import { mande } from 'mande'
import type { Configuration } from '../models/core'

const configuration = mande(`${import.meta.env.VITE_BACKEND_URL}/api/configuration`)

export function getConfiguration() {
    return configuration.get<Configuration>('/')
}

export function modifyConfiguration({ data }: { data: Partial<Configuration> }) {
    return configuration.patch<Configuration>('/useless-id-to-fool-drf/', data)
}

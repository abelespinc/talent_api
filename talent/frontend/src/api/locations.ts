import { mande } from 'mande'
import { prepareObjectForQuery } from '../utils/objects'
import type { LocationForSearch } from '../models/locations'

const locations = mande(`${import.meta.env.VITE_BACKEND_URL}/api/locations`)

export function getLocationsForSearch({ name = '' } = {}) {
    return locations.get<LocationForSearch[]>('/search/', { query: prepareObjectForQuery({ name }) })
}

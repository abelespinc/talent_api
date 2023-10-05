export type LocationType = 'CITY' | 'SUBREGION'

export interface LocationForSearch {
    id: string
    type: LocationType
    name: string
}

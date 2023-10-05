import { mande } from 'mande'
import type { Offer, OfferDetailed } from '../models/offers'
import type { GetOffersBody } from '../models/api/offers'
import type { PaginatedResponse } from '../models/paginatedQuery'
import { flattenObject, prepareObjectForQuery } from '../utils/objects'
import type { LocationType } from '../models/locations'

const offers = mande(`${import.meta.env.VITE_BACKEND_URL}/api/offers`)

export function getOffers({ search = undefined, limit = undefined, offset = 0 }: GetOffersBody) {
    const flatSearch = flattenObject(search || {})
    const preparedQuery = prepareObjectForQuery({
        ...flatSearch,
        id: undefined,
        type: undefined,
        locationId: flatSearch.id,
        locationType: flatSearch.type,
    })

    return offers.get<PaginatedResponse<Offer>>('/', { query: { ...preparedQuery, limit, offset } })
}

export function getOffer(offerId: string) {
    return offers.get<OfferDetailed>(`${offerId}/`)
}

export function assignStandardLocationToOffer(offerId: string, location: { id: string; type: LocationType }) {
    return offers.patch<void>(`${offerId}/standard-location/`, { location })
}

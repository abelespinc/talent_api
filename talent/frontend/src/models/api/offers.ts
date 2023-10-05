import type { PaginatedQueryParams } from '.'
import type { LocationType } from '../locations'
import type { OfferSearchFilters } from '../offers'

export interface GetOffersBody extends PaginatedQueryParams {
    search?: {
        job: string
        location: { id: string; type: LocationType }
        filters: Record<OfferSearchFilters, string>
    }
}

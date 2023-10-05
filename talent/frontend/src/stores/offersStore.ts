import { defineStore } from 'pinia'
import { getOffer, getOffers } from '../api/offers'
import { usePaginatedQuery } from '../hooks/usePaginatedQuery'
import type { Offer, OfferDetailed, OfferSearchFilters } from '../models/offers'
import type { OffersSearch } from '../models/searches'
import { saveSearch } from '../utils/searches'

const PAGE_SIZE = 10

const INITIAL_SEARCH = { job: '', location: undefined }
const INITIAL_FILTERS: Record<OfferSearchFilters, any> = {
    temporality: undefined,
    attendance: undefined,
    contractType: undefined,
    competitor: undefined,
    company: undefined,
    postingDate: undefined,
    minSalary: undefined,
    status: undefined,
    duplicates: undefined,
    titleAndDescription: undefined,
}

const defineOffersStore = defineStore('offers', {
    state: () => ({
        initialized: false,
        query: usePaginatedQuery(getOffers, {
            search: { ...structuredClone(INITIAL_SEARCH), ...structuredClone(INITIAL_FILTERS) },
            limit: PAGE_SIZE,
            offset: 0,
        }),
        selectedOffer: undefined as OfferDetailed | undefined,
    }),

    getters: {
        offers(): Offer[] {
            return this.query.data
        },
        filters(): typeof INITIAL_SEARCH & typeof INITIAL_FILTERS {
            return this.query.params.search
        },
    },

    actions: {
        async init() {
            await this.query.fetchNextPage(true)

            if (this.offers.length) {
                this.setSelectedOfferFromOfferId(this.offers[0].id)
            }

            this.initialized = true
        },
        async onFilterChange(filterName: string, filterValue: any) {
            this.selectedOffer = undefined
            this.query.data = []
            this.query.params.search[filterName] = filterValue
            this.init()
        },
        async setSelectedOfferFromOfferId(offerId: string) {
            this.selectedOffer = await getOffer(offerId)
        },
        saveSearch() {
            /**
             * Save the current search and filters to localStorage
             */
            saveSearch({ search: this.query.params.search, date: new Date().toISOString() })
        },
        async restoreSearch(search: OffersSearch) {
            this.query.params.search = search
            this.init()
        },
    },
})

export async function useOffersStore() {
    const store = defineOffersStore()

    if (!store.initialized) {
        await store.init()
    }

    return store
}

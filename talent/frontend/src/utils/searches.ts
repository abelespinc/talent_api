import type { RecentSearch } from '../models/searches'

export const MAX_RECENT_SEARCHES = 50
export const RECENT_SEARCH_STORAGE_KEY = 'recentSearches'

export function saveSearch(search: RecentSearch) {
    /**
     * Save the given search and filters to localStorage
     */
    const recentSearches = localStorage.getItem(RECENT_SEARCH_STORAGE_KEY)

    if (recentSearches) {
        const parsedRecentSearches = JSON.parse(recentSearches)

        if (parsedRecentSearches.length >= MAX_RECENT_SEARCHES) {
            parsedRecentSearches.length = MAX_RECENT_SEARCHES - 1
        }

        localStorage.setItem(RECENT_SEARCH_STORAGE_KEY, JSON.stringify([...parsedRecentSearches, search]))
    } else {
        localStorage.setItem(RECENT_SEARCH_STORAGE_KEY, JSON.stringify([search]))
    }
}

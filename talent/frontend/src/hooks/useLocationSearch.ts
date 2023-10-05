import type { Ref } from 'vue'
import { computed, reactive, toRefs } from 'vue'

import { watchDebounced } from '@vueuse/core'

import type { LocationForSearch } from '../models/locations'
import { getLocationsForSearch } from '../api/locations'

export function useLocationSearch(searchText: Ref<string>) {
    const state = reactive({
        locations: [] as LocationForSearch[],
        isEmptySearch: false,
    })

    watchDebounced(
        searchText,
        async () => {
            state.isEmptySearch = false

            state.locations = await getLocationsForSearch({ name: searchText.value })

            if (state.locations.length === 0) {
                state.isEmptySearch = true
            }
        },
        { debounce: 300, maxWait: 1000 }
    )

    return {
        ...toRefs(state),
        cities: computed(() => state.locations.filter((location) => location.type === 'CITY')),
        subregions: computed(() => state.locations.filter((location) => location.type === 'SUBREGION')),
    }
}

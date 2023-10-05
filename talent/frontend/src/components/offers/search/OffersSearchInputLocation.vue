<template>
    <div class="dropdown">
        <OffersSearchInput
            :model-value="searchText || selectedLocationName"
            :label="$t('offers.search.where')"
            :max-width="350"
            placeholder="Barcelona"
            @update:model-value="searchText = $event"
        ></OffersSearchInput>

        <ul ref="dropdownMenuEL" class="dropdown-menu mt-3" :class="{ show: isDropdownMenuVisible }">
            <div v-show="isEmptySearch" class="px-4 py-4">
                <span class="fw-semibold text-muted">{{ $t('locations.search.badSearch') }}</span>
            </div>

            <li v-show="subregions.length" class="mb-n3">
                <b class="dropdown-header fs-5">{{ $t('locations.type.subregion', 2) }}</b>
            </li>
            <li v-for="subregion in subregions" :key="subregion.id">
                <button type="button" class="dropdown-item" @click="onLocationClick(subregion)">
                    {{ subregion.name }}
                </button>
            </li>

            <li v-show="cities.length" class="mb-n3 border-top">
                <b class="dropdown-header fs-5">{{ $t('locations.type.city', 2) }}</b>
            </li>
            <li v-for="city in cities" :key="city.id">
                <button type="button" class="dropdown-item" @click="onLocationClick(city)">
                    {{ city.name }}
                </button>
            </li>
        </ul>
    </div>
</template>

<script setup lang="ts">
// Vue imports
import { computed, ref } from 'vue'

// Third-party imports
import { onClickOutside } from '@vueuse/core'

// Component imports
import OffersSearchInput from './OffersSearchInput.vue'
import type { LocationForSearch, LocationType } from '../../../models/locations'
import { useLocationSearch } from '../../../hooks/useLocationSearch'

// Project imports

// ---------------------------------------- //

// Props and emits definition
// defineProps({})
defineEmits([])
const vModel = defineModel<{ id: string; type: LocationType }>({ required: true })

// ---------------------------------------- //

// Component-specific code
const dropdownMenuEL = ref<HTMLElement | null>(null)
const searchText = ref('')
const selectedLocationName = ref('')

const { locations, cities, subregions, isEmptySearch } = useLocationSearch(searchText)
const isDropdownMenuVisible = computed(() => locations.value.length > 0 || isEmptySearch.value)

function onLocationClick(location: LocationForSearch) {
    searchText.value = ''
    selectedLocationName.value = location.name
    vModel.value = { id: location.id, type: location.type }
    locations.value = []
}

onClickOutside(dropdownMenuEL, () => {
    if (isDropdownMenuVisible.value) {
        isEmptySearch.value = false
        locations.value = []
        searchText.value = ''
    }
})
</script>

<style lang="scss" scoped></style>

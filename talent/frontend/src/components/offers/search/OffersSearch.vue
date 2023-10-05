<template>
    <div class="d-flex flex-column align-items-center gap-3">
        <form
            class="d-flex w-100 justify-content-between align-items-center gap-3 flex-column flex-lg-row flex-grow-1"
            @submit.prevent="onFormSubmit()"
        >
            <div class="d-flex gap-3 align-items-center flex-grow-1">
                <OffersSearchInput
                    v-model="offersStore.filters.job"
                    :label="$t('offers.search.what')"
                    placeholder="Software developer"
                    class="flex-grow-1"
                ></OffersSearchInput>
                <OffersSearchInputLocation v-model="offersStore.filters.location"></OffersSearchInputLocation>

                <button type="submit" class="btn btn-primary rounded-3 py-3 px-4 fw-semibold text-nowrap">
                    {{ $t('offers.search.searchOffers') }}
                </button>
            </div>

            <div>
                <router-link
                    :to="{ name: 'recentSearches' }"
                    class="btn btn-outline-primary rounded-3 py-3 px-4 fw-semibold"
                >
                    {{ $t('recentSearches.recentSearches') }}
                </router-link>
            </div>
        </form>

        <OffersSearchFilters v-if="showFilters"></OffersSearchFilters>
    </div>
</template>

<script setup lang="ts">
// Vue imports
import {} from 'vue'

// Third-party imports

// Component imports
import OffersSearchInput from './OffersSearchInput.vue'
import OffersSearchFilters from './filters/OffersSearchFilters.vue'

// Project imports
// ---------------------------------------- //
import { useOffersStore } from '../../../stores/offersStore'
import OffersSearchInputLocation from './OffersSearchInputLocation.vue'

// Props and emits definition
defineProps({
    showFilters: { type: Boolean, required: false, default: false },
})
defineEmits([])
// ---------------------------------------- //

// Component-specific code
const offersStore = await useOffersStore()

async function onFormSubmit() {
    offersStore.selectedOffer = undefined
    offersStore.query.data = []
    await offersStore.query.fetchNextPage(true)

    if (offersStore.offers.length) {
        offersStore.setSelectedOfferFromOfferId(offersStore.offers[0].id)
    } else {
        offersStore.selectedOffer = undefined
    }

    offersStore.saveSearch()
}
</script>

<style lang="scss" scoped>
@import 'src/assets/scss/mixins';

button {
    width: 100%;

    @include media-breakpoint-up(lg) {
        width: auto;
    }
}
</style>

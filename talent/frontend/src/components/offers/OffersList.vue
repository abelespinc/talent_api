<template>
    <VirtualInfiniteList
        v-slot="{ item: offer }"
        :items="offersStore.query.data"
        :item-height="220"
        @reach-bottom="onReachBottom()"
    >
        <OfferCard v-if="!showPlaceholders" :offer="offer" class="mx-auto mx-lg-0"></OfferCard>
        <div v-else class="placeholder-glow" style="height: var(--offer-card-height)">
            <div class="card placeholder bg-white h-100 w-100">
                <div class="card-body"></div>
            </div>
        </div>
    </VirtualInfiniteList>
</template>

<script setup lang="ts">
// Vue imports

// Third-party imports

// Component imports
import { computed } from 'vue'
import OfferCard from './OfferCard.vue'
import VirtualInfiniteList from '../base/VirtualInfiniteList.vue'

// Project imports
import { useOffersStore } from '../../stores/offersStore'

// ---------------------------------------- //

// Props and emits definition
// defineProps({})
defineEmits([])
// ---------------------------------------- //

// Component-specific code
const offersStore = await useOffersStore()
const { fetchNextPage } = offersStore.query
const showPlaceholders = computed(() => offersStore.query.data.length === 0 && offersStore.query.isLoading)

function onReachBottom() {
    if (offersStore.query.moreDataAvailable) {
        fetchNextPage()
    }
}
</script>

<style lang="scss" scoped></style>

<template>
    <div class="d-flex flex-column gap-3">
        <OffersSearch show-filters></OffersSearch>

        <div>
            <div class="row">
                <div class="col-lg-4">
                    <OffersCount class="mb-2 pb-1 mt-n1 border-bottom border-primary border-opacity-25"></OffersCount>
                    <OffersList></OffersList>
                </div>
                <div class="col-lg-8 d-none d-lg-block">
                    <OfferDetailCard
                        v-if="offersStore.selectedOffer"
                        :offer="offersStore.selectedOffer"
                    ></OfferDetailCard>

                    <div v-else-if="offersStore.query.isLoading" class="placeholder-glow h-100">
                        <div class="card placeholder bg-white h-100 w-100">
                            <div class="card-body"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
// Vue imports
import {} from 'vue'

// Third-party imports
import { useRoute, useRouter } from 'vue-router'

// Component imports
import OffersSearch from '../components/offers/search/OffersSearch.vue'
import OffersList from '../components/offers/OffersList.vue'
import OfferDetailCard from '../components/offers/OfferDetailCard.vue.vue'
import OffersCount from '../components/offers/OffersCount.vue'

// Project imports
import { useOffersStore } from '../stores/offersStore'

// ---------------------------------------- //

// Props and emits definition
// defineProps({})
defineEmits([])
// ---------------------------------------- //

// Component-specific code
const route = useRoute()
const router = useRouter()
const offersStore = await useOffersStore()

await router.isReady()

if (route.query.company) {
    offersStore.onFilterChange('company', route.query.company)
}
</script>

<style lang="scss" scoped></style>

<template>
    <div
        :class="{
            'border-primary': offerIsSelected && !offer.company.isCompetitor,
            'border-danger': offerIsSelected && offer.company.isCompetitor,
            'border-transparent': !offerIsSelected,
        }"
        class="card border border-2 cursor-pointer"
        @click="onCardClick()"
    >
        <div class="card-body d-flex flex-column justify-content-between gap-2">
            <div class="d-flex flex-column">
                <div class="d-flex justify-content-between gap-2">
                    <div class="job-name">
                        <span class="fw-bold">{{ offerName }}</span>
                        <small v-if="offer.duplicatesCount" class="fw-light text-nowrap">
                            ({{ offer.duplicatesCount }} {{ $t('offers.duplicates', offer.duplicatesCount) }})
                        </small>
                    </div>
                    <div v-if="offer.company.isCompetitor">
                        <CompaniesCompetitorBadge></CompaniesCompetitorBadge>
                    </div>
                </div>
                <div class="offer-main-info">
                    <CompanyCompetitorIcon
                        v-if="offer.company.isCompetitor"
                        is-competitor
                        class="d-inline-block me-2"
                    ></CompanyCompetitorIcon>
                    <i v-else class="bi-briefcase-fill me-2"></i>
                    <span>{{ offer.company.name }}</span>
                </div>
                <div class="offer-main-info">
                    <i class="bi-geo-alt-fill me-2"></i>
                    <span>{{ offer.location }}</span>
                </div>
            </div>

            <OfferInfoBadges :offer="offer"></OfferInfoBadges>

            <div>
                <small class="fw-semibold">Publicado el {{ offerPostingDate }}</small>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
// Vue imports
import type { PropType } from 'vue'
import { computed } from 'vue'

// Third-party imports

// Component imports
import OfferInfoBadges from './OfferInfoBadges.vue'
import CompaniesCompetitorBadge from '../companies/CompaniesCompetitorBadge.vue'
import CompanyCompetitorIcon from '../companies/CompanyCompetitorIcon.vue'

// Project imports
import type { Offer } from '../../models/offers'
import { useOffersStore } from '../../stores/offersStore'
import { truncateText } from '../../utils/truncateText'
import { getOffer } from '../../api/offers'
// ---------------------------------------- //

// Props and emits definition
const props = defineProps({
    offer: { type: Object as PropType<Offer>, required: true },
})
defineEmits([])
// ---------------------------------------- //

// Component-specific code
const offersStore = await useOffersStore()

const offerName = computed(() => truncateText(props.offer.job, 45))
const offerPostingDate = computed(() => new Date(props.offer.postingDate).toLocaleDateString())
const offerIsSelected = computed(() => props.offer.id === offersStore.selectedOffer?.id)

const onCardClick = () => {
    getOffer(props.offer.id).then((offer) => {
        offersStore.selectedOffer = offer
    })
}
</script>

<style lang="scss" scoped>
@import 'src/assets/scss/mixins';

.card {
    height: var(--offer-card-height);
    max-width: var(--offer-card-max-width);
}

.job-name {
    line-height: 1.2;

    & > span {
        font-size: 1.05rem;

        @include media-breakpoint-up(xxl) {
            font-size: 1.1rem;
        }
    }
}

.offer-main-info {
    font-size: 0.9rem;

    @include media-breakpoint-up(xxl) {
        font-size: 1rem;
    }
}
</style>

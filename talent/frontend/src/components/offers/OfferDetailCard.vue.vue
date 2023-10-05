<template>
    <div>
        <div class="card border border-2" :class="offer.company.isCompetitor ? 'border-danger' : 'border-transparent'">
            <div class="card-body d-flex flex-column gap-2">
                <div class="d-flex flex-column border-2 border-bottom border-light pb-2">
                    <div class="d-flex justify-content-between gap-2 flex-wrap flex-xxl-nowrap mb-2">
                        <div>
                            <span class="fw-bold fs-5">{{ offer.job }}</span>
                            <OfferDetailCardSimilarity
                                v-if="offer.similarities.job"
                                :similarity="offer.similarities.job"
                            ></OfferDetailCardSimilarity>
                            <div>
                                <CompanyCompetitorIcon
                                    v-if="offer.company.isCompetitor"
                                    is-competitor
                                    class="d-inline-block me-2"
                                ></CompanyCompetitorIcon>
                                <i v-else class="bi-briefcase-fill me-2"></i>
                                <span>{{ offer.company.name }}</span>
                            </div>
                            <div>
                                <i class="bi-geo-alt-fill me-2"></i>
                                <span>{{ offer.location.name }}</span>
                                <OfferDetailCardSimilarity
                                    v-if="offer.similarities.location"
                                    :similarity="offer.similarities.location"
                                ></OfferDetailCardSimilarity>
                                <button
                                    v-show="!offer.location.hasStandardLocation"
                                    type="button"
                                    class="btn btn-sm btn-outline-danger fw-semibold ms-3"
                                    style="--bs-btn-border-width: 2px"
                                    @click="showSelectLocationModal = true"
                                >
                                    {{ $t('locations.assignLocation') }}
                                </button>
                            </div>
                        </div>

                        <div v-if="offer.company.isCompetitor">
                            <CompaniesCompetitorBadge></CompaniesCompetitorBadge>
                        </div>
                        <div v-else>
                            <button
                                class="btn btn-sm btn-outline-danger fw-semibold rounded-3 text-nowrap"
                                style="--bs-btn-border-width: 2px"
                                @click="onMakeCompetitorClick()"
                            >
                                {{ $t('companies.markAsCompetitor') }}
                            </button>
                        </div>
                    </div>

                    <div v-if="offer.url" class="mt-2 fw-semibold">
                        <div class="d-flex justify-content-between flex-wrap">
                            <a :href="offer.url" target="_blank" class="d-flex align-items-center gap-2">
                                <span>{{ $t('offers.seeIn') }}</span>
                                <span class="text-capitalize">{{ offer.source }}</span>
                                <i class="bi-box-arrow-up-right small"></i>
                            </a>

                            <div class="mt-2">
                                <a
                                    v-for="(duplicate, i) in offer.duplicates"
                                    :key="i"
                                    :href="duplicate.url"
                                    target="_blank"
                                    class="d-flex align-items-center gap-2"
                                >
                                    <span>{{ $t('offers.seeDuplicateIn') }}</span>
                                    <span class="text-capitalize">{{ duplicate.source }}</span>
                                    <i class="bi-box-arrow-up-right small"></i>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>

                <div ref="offerBody" class="offer-body" :class="{ 'pe-2': offerBodyScrollIsShown }">
                    <div class="row border-2 border-bottom border-light pb-2 mb-2">
                        <div class="col-lg-7">
                            <div class="d-flex flex-column">
                                <span class="fw-bold fs-5 mb-3">{{ $t('offers.job.details') }}</span>

                                <template v-if="offer.salary.min || offer.salary.max">
                                    <span class="fw-bold">{{ $t('offers.job.salary') }}</span>
                                    <div class="mb-3">
                                        <i class="bi-cash-stack me-2"></i>
                                        <span>{{ offerSalary }}</span>
                                        <i v-if="offer.salary.isAi" class="bi-robot text-secondary ms-2"></i>
                                    </div>
                                </template>

                                <span class="fw-bold">{{ $t('offers.job.type') }}</span>
                                <div>
                                    <i class="bi-clock me-2"></i>
                                    <span>{{ offerTemporality }}</span>
                                    <OfferDetailCardSimilarity
                                        v-if="offer.similarities.temporality"
                                        :similarity="offer.similarities.temporality"
                                    ></OfferDetailCardSimilarity>
                                </div>
                                <div>
                                    <i class="bi-person me-2"></i>
                                    <span>{{ offerAttendance }}</span>
                                    <OfferDetailCardSimilarity
                                        v-if="offer.similarities.attendance"
                                        :similarity="offer.similarities.attendance"
                                    ></OfferDetailCardSimilarity>
                                </div>
                                <div>
                                    <i class="bi-file-text me-2"></i>
                                    <span>{{ offerContractType }}</span>
                                    <OfferDetailCardSimilarity
                                        v-if="offer.similarities.contractType"
                                        :similarity="offer.similarities.contractType"
                                    ></OfferDetailCardSimilarity>
                                </div>
                            </div>
                        </div>
                        <div v-if="offer.skills.length" class="col-lg-5">
                            <div class="d-flex flex-column">
                                <span class="fw-bold fs-5 mb-3">{{ $t('offers.job.skills') }}</span>

                                <ul>
                                    <li v-for="(skill, i) in offer.skills" :key="i">{{ skill }}</li>
                                </ul>
                            </div>
                        </div>
                    </div>

                    <div class="d-flex flex-column border-2">
                        <span class="fw-bold fs-5 mb-3">{{ $t('offers.job.completeDescription') }}</span>

                        <p class="border border-primary border-opacity-25 p-3 rounded-3" v-html="offer.description"></p>
                    </div>
                </div>
            </div>
        </div>

        <UndoPopup
            v-if="showUndoMakeCompetitor"
            @undo="onUndoMakeCompetitor()"
            @finish="showUndoMakeCompetitor = false"
        >
            {{ $t('companies.youMarkedAsCompetitor', { company: offer.company.name }) }}
        </UndoPopup>

        <LocationSearchModal
            v-model="newStandardLocation"
            v-model:trigger="showSelectLocationModal"
            @update:model-value="onSelectStandardLocation()"
        ></LocationSearchModal>
    </div>
</template>

<script setup lang="ts">
// Vue imports
import type { PropType } from 'vue'
import { computed, ref } from 'vue'

// Third-party imports
import { useI18n } from 'vue-i18n'

// Component imports
import CompaniesCompetitorBadge from '../companies/CompaniesCompetitorBadge.vue'
import CompanyCompetitorIcon from '../companies/CompanyCompetitorIcon.vue'
import UndoPopup from '../core/UndoPopup.vue'
import OfferDetailCardSimilarity from './OfferDetailCardSimilarity.vue'

// Project imports
import type { OfferDetailed } from '../../models/offers'
import { camelize } from '../../utils/camelize'
import { salaryToString } from '../../utils/offers'
import { modifyCompany } from '../../api/companies'
import { useOffersStore } from '../../stores/offersStore'
import { useElementDistanceToBottom } from '../../hooks/useElementDistanceToBottom'
import LocationSearchModal from '../locations/LocationSearchModal.vue'
import type { LocationForSearch } from '../../models/locations'
import { assignStandardLocationToOffer } from '../../api/offers'

// ---------------------------------------- //

// Props and emits definition
const props = defineProps({
    offer: { type: Object as PropType<OfferDetailed>, required: true },
})
defineEmits([])
// ---------------------------------------- //

// Component-specific code
const { t } = useI18n()

const showSelectLocationModal = ref(false)
const newStandardLocation = ref<LocationForSearch>()

const offerTemporality = computed(() => t(`offers.search.filters.temporality.${camelize(props.offer.temporality)}`))
const offerAttendance = computed(() => t(`offers.search.filters.attendance.${camelize(props.offer.attendance)}`))
const offerContractType = computed(() => t(`offers.search.filters.contractType.${camelize(props.offer.contractType)}`))
const offerSalary = computed(() => salaryToString(props.offer.salary))
const showUndoMakeCompetitor = ref(false)

const offerBody = ref<HTMLElement | null>(null)
const offerBodyHeight = useElementDistanceToBottom(offerBody)
const offerBodyScrollIsShown = computed(() => (offerBody.value?.scrollHeight || 0) > offerBodyHeight.value)

const offersStore = await useOffersStore()

function modifCompanyCompetition(isCompetitor: boolean) {
    return modifyCompany({ companyId: props.offer.company.id, data: { isCompetitor } }).then(() => {
        const companyName = props.offer.company.name

        offersStore.offers
            .filter((offer) => offer.company.name === companyName)
            .forEach((offer) => {
                offer.company.isCompetitor = isCompetitor
            })

        if (offersStore.selectedOffer) {
            offersStore.selectedOffer.company.isCompetitor = isCompetitor
        }
    })
}

async function onMakeCompetitorClick() {
    await modifCompanyCompetition(true)
    showUndoMakeCompetitor.value = true
}

async function onUndoMakeCompetitor() {
    await modifCompanyCompetition(false)
    showUndoMakeCompetitor.value = false
}

async function onSelectStandardLocation() {
    if (newStandardLocation.value) {
        await assignStandardLocationToOffer(props.offer.id, newStandardLocation.value)

        if (offersStore.selectedOffer) {
            offersStore.selectedOffer.location.hasStandardLocation = true
        }
    }
}
</script>

<style lang="scss" scoped>
@import 'src/assets/scss/mixins';

.offer-body {
    @include scrollbar;

    // Height - card bottom padding - body padding bottom - card border width
    max-height: calc(v-bind('`${offerBodyHeight}px`') - var(--bs-card-spacer-y) - var(--body-padding-y) - 2px);
    overflow-y: auto;
    overflow-x: hidden;
}

.duplicate-offer-url {
    font-size: 0.95rem;
    opacity: 0.9;
}
</style>

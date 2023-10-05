<template>
    <div class="d-flex flex-wrap gap-1">
        <OfferInfoBadge v-if="showSalary" info-type="salary" :info="offer.salary"></OfferInfoBadge>
        <OfferInfoBadge info-type="temporality" :info="offer.temporality"></OfferInfoBadge>
        <OfferInfoBadge info-type="attendance" :info="offer.attendance"></OfferInfoBadge>
        <OfferInfoBadge v-if="offer.contractType" info-type="contractType" :info="offer.contractType"></OfferInfoBadge>
    </div>
</template>

<script setup lang="ts">
// Vue imports
import type { PropType } from 'vue'
import { computed } from 'vue'

// Third-party imports

// Component imports
import OfferInfoBadge from './OfferInfoBadge.vue'

// Project imports
import type { Offer } from '../../models/offers'
// ---------------------------------------- //

// Props and emits definition
const props = defineProps({
    offer: { type: Object as PropType<Offer>, required: true },
})
defineEmits([])
// ---------------------------------------- //

// Component-specific code
const showSalary = computed(() => props.offer.salary && (props.offer.salary.min || props.offer.salary.max))
</script>

<style lang="scss" scoped></style>

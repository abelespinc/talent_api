<template>
    <span class="badge" :class="offerCompanyIsCompetitor ? 'text-bg-danger' : 'text-bg-secondary'">
        <i :class="infoParams.icon" class="me-2"></i>
        <span>{{ text }}</span>
    </span>
</template>

<script setup lang="ts">
// Vue imports
import type { PropType } from 'vue'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

// Third-party imports

// Component imports

// Project imports
import type { OfferInfoType } from '../../models/offers'
import { camelize } from '../../utils/camelize'
import { salaryToString } from '../../utils/offers'
// ---------------------------------------- //

// Props and emits definition
const props = defineProps({
    info: { type: [String, Object], required: true },
    infoType: { type: String as PropType<OfferInfoType>, required: true },
    offerCompanyIsCompetitor: { type: Boolean, required: false, default: false },
})
defineEmits([])
// ---------------------------------------- //

// Component-specific code
const { t } = useI18n()

const allInfoParams: Record<OfferInfoType, any> = {
    attendance: {
        parser: (rawInfo: string) => t(`offers.search.filters.attendance.${camelize(rawInfo)}`),
        icon: 'bi-person',
    },
    temporality: {
        parser: (rawInfo: string) => t(`offers.search.filters.temporality.${camelize(rawInfo)}`),
        icon: 'bi-clock',
    },
    contractType: {
        parser: (rawInfo: string) => t(`offers.search.filters.contractType.${camelize(rawInfo)}`),
        icon: 'bi-file-text',
    },
    salary: {
        parser: (rawInfo: string) => salaryToString(rawInfo),
        icon: 'bi-cash-stack',
    },
}
const infoParams = computed(() => allInfoParams[props.infoType])
const text = computed(() => infoParams.value.parser(props.info))
</script>

<style lang="scss" scoped></style>

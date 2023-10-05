<template>
    <div>
        <div>
            <span class="fw-semibold mb-0 d-inline">
                <template v-if="offersTotalCount !== undefined">
                    {{ offersTotalCount.toLocaleString() }} {{ $t('offers.offers', offersTotalCount) }}
                    <template v-if="companyFilter">
                        {{ $t('offers.publishedBy', offersTotalCount) }} {{ companyFilter }}
                    </template>
                    <template v-else>{{ $t('offers.publishedWithCurrentFilters', offersTotalCount) }}</template>
                </template>
                <span v-else class="placeholder w-25 placeholder-glow"></span>
            </span>
        </div>
        <div v-if="companyFilter" class="link-danger cursor-pointer" @click="onClearCompanyFilterClick()">
            <i class="bi-trash3 pe-1 cursor-pointer"></i>
            <span>{{ $t('offers.search.filters.clearCompanyFilter') }}</span>
        </div>
    </div>
</template>

<script setup lang="ts">
// Vue imports
import { computed } from 'vue'
import { useOffersStore } from '../../stores/offersStore'

// Third-party imports

// Component imports

// Project imports
// ---------------------------------------- //

// Props and emits definition
// defineProps({})
defineEmits([])
// ---------------------------------------- //

// Component-specific code
const offersStore = await useOffersStore()
const companyFilter = computed(() => offersStore.filters.company)
const offersTotalCount = computed(() =>
    offersStore.query.totalCount !== undefined ? offersStore.query.totalCount : offersStore.query.totalCount
)

async function onClearCompanyFilterClick() {
    await offersStore.onFilterChange('company', undefined)
}
</script>

<style lang="scss" scoped></style>

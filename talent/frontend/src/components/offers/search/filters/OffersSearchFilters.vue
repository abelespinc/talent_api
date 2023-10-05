<template>
    <div class="filters-wrapper pb-2">
        <div class="d-flex align-items-center gap-2">
            <OffersSearchFilter
                v-for="(filter, i) in searchFilters"
                :key="i"
                :filter="filter"
                class="w-auto"
            ></OffersSearchFilter>

            <div class="form-floating">
                <input
                    id="minSalaryInput"
                    v-model.number.lazy="minSalary"
                    type="number"
                    min="0"
                    step="500"
                    :placeholder="t('offers.search.filters.minSalary.name')"
                    class="form-control bg-white small"
                />
                <label for="minSalaryInput" class="fw-semibold">{{ t('offers.search.filters.minSalary.name') }}</label>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
// Vue imports
import { computed } from 'vue'

// Third-party imports
import { useI18n } from 'vue-i18n'

// Component imports
import OffersSearchFilter from './OffersSearchFilter.vue'

// Project imports
import { searchFilters } from '../../../../config/searchFilters'
import { useOffersStore } from '../../../../stores/offersStore'
// ---------------------------------------- //

// Props and emits definition
// defineProps({})
defineEmits([])
// ---------------------------------------- //

// Component-specific code
const { t } = useI18n()

const offersStore = await useOffersStore()
// Use computed for vModel for clarity
const minSalary = computed({
    get: () => offersStore.filters.minSalary,
    set: (newValue) => offersStore.onFilterChange('minSalary', newValue),
})
</script>

<style lang="scss" scoped>
@import 'src/assets/scss/mixins';

.filters-wrapper {
    @include scrollbar;

    overflow-x: auto;

    & > .d-flex > * {
        flex-shrink: 0;
    }
}

.form-floating {
    max-width: 145px;

    & > input {
        font-size: var(--filter-font-size);
        height: calc(var(--filter-font-size) * 2.75) !important;
        padding-top: calc(var(--filter-font-size) * 1.3) !important;
        padding-bottom: calc(var(--filter-font-size) * 0.7) !important;
        border: 0 !important;
        box-shadow: none !important;

        & + label {
            font-size: var(--filter-font-size);
            padding-top: calc(var(--filter-font-size) * 0.6);
            padding-bottom: calc(var(--filter-font-size) * 0.5);
        }

        &::placeholder {
            font-size: var(--filter-font-size);
        }
    }
}
</style>

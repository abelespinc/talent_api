<template>
    <div
        v-auto-animate="{ easing: 'ease-out', duration: 100 }"
        :class="{ 'pe-3': optionSelected }"
        class="d-flex align-items-center bg-white rounded-3"
    >
        <select
            v-model="vModel"
            :class="{ 'text-secondary': optionSelected }"
            class="bg-transparent form-select fw-semibold"
        >
            <option
                v-for="(option, i) in filter.options"
                :key="i"
                :value="option.value"
                :hidden="option.hidden"
                :disabled="option.disabled"
                :selected="option.selected"
                class="text-body"
            >
                {{ option.text }}
            </option>
        </select>
        <i v-if="optionSelected" class="bi-trash3 text-danger cursor-pointer" @click="onClearClick()"></i>
    </div>
</template>

<script setup lang="ts">
// Vue imports
import { computed } from 'vue'
import type { PropType } from 'vue'

// Third-party imports

// Component imports

// Project imports
import type { OffersSearchFilter } from '../../../../models/offers'
import { useOffersStore } from '../../../../stores/offersStore'
// ---------------------------------------- //

// Props and emits definition
const props = defineProps({
    filter: { type: Object as PropType<OffersSearchFilter>, required: true },
})
defineEmits([])
// ---------------------------------------- //

// Component-specific code
const offersStore = await useOffersStore()
// Use computed for vModel for clarity
const vModel = computed({
    get: () => offersStore.filters[props.filter.name],
    set: (newValue) => offersStore.onFilterChange(props.filter.name, newValue),
})

const onClearClick = () => {
    vModel.value = undefined
}
const optionSelected = computed(() => vModel.value !== undefined)
</script>

<style lang="scss" scoped>
select {
    font-size: var(--filter-font-size);

    &:focus-visible {
        outline: none;
    }

    &:focus {
        box-shadow: none;
    }
}

i {
    font-size: 1.1rem;
}
</style>

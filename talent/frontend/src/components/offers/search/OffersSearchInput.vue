<template>
    <div class="bg-white rounded-3 py-3 px-4 shadow-sm w-100 d-flex align-items-center">
        <label class="me-3 fw-bold" :for="inputId">{{ label }}</label>
        <input :id="inputId" v-model="vModel" type="text" class="border-0 flex-grow-1" :placeholder="placeholder" />
    </div>
</template>

<script setup lang="ts">
// Vue imports
import { computed } from 'vue'

// Third-party imports
import { useVModel } from '@vueuse/core'

// Component imports

// Project imports
import { randomString } from '../../../utils/randomString'

// ---------------------------------------- //

// Props and emits definition
const props = defineProps({
    modelValue: { type: String, required: false, default: '' },
    label: { type: String, required: true },
    placeholder: { type: String, required: true },
    maxWidth: { type: Number, required: false, default: undefined },
})
const emit = defineEmits(['update:modelValue'])
// ---------------------------------------- //

// Component-specific code
const vModel = useVModel(props, 'modelValue', emit)
const inputId = randomString()
const maxWidthCss = computed(() => (props.maxWidth ? `${props.maxWidth}px` : 'auto'))
</script>

<style lang="scss" scoped>
@import 'src/assets/scss/mixins';

div {
    @include media-breakpoint-up(lg) {
        min-width: 300px;
        max-width: v-bind('maxWidthCss');
    }
}

label {
    width: 50px;

    @include media-breakpoint-up(lg) {
        width: auto;
    }
}

input {
    &:focus-visible {
        outline: none;
    }
}
</style>

<template>
    <div class="position-absolute text-bg-dark rounded-3 shadow">
        <div class="d-flex align-items-center justify-content-between gap-5 py-3 px-4">
            <span class="fw-semibold text-wrap">
                <slot></slot>
            </span>
            <span class="text-warning fw-bold cursor-pointer" @click="onUndoClick()">{{ $t('undo') }}</span>
        </div>
        <div class="progress" style="height: 5px">
            <div
                class="progress-bar bg-warning"
                role="progressbar"
                :style="{ width: `${bottomBorderWidthPercentage}%` }"
            ></div>
        </div>
    </div>
</template>

<script setup lang="ts">
// Vue imports
import { ref } from 'vue'

// Third-party imports

// Component imports

// Project imports
// ---------------------------------------- //

// Props and emits definition
const props = defineProps({
    duration: { type: Number, required: false, default: 5000 }, // In ms
})
const emit = defineEmits(['undo', 'finish'])
// ---------------------------------------- //

// Component-specific code
const progressUpdateInterval = 50
const bottomBorderWidthPercentage = ref(100)

const onUndoClick = () => {
    emit('undo')
}

const interval = setInterval(() => {
    bottomBorderWidthPercentage.value -= 100 / (props.duration / progressUpdateInterval)

    if (bottomBorderWidthPercentage.value <= 0) {
        clearInterval(interval)
        emit('finish')
    }
}, progressUpdateInterval)

const resetPopup = () => {
    bottomBorderWidthPercentage.value = 100
}
</script>

<style lang="scss" scoped>
.position-absolute {
    bottom: 20px;
    right: 20px;
}
</style>

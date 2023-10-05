<template>
    <div class="icon-container text-primary">
        <svg viewBox="0 0 512 512" focusable="false" class="d-block">
            <path
                d="M416 398.9c58.5-41.1 96-104.1 96-174.9C512 100.3 397.4 0 256 0S0 100.3 0 224c0 70.7 37.5 133.8 96 174.9c0 .4 0 .7 0 1.1v64c0 26.5 21.5 48 48 48h48V464c0-8.8 7.2-16 16-16s16 7.2 16 16v48h64V464c0-8.8 7.2-16 16-16s16 7.2 16 16v48h48c26.5 0 48-21.5 48-48V400c0-.4 0-.7 0-1.1zM224 256c0 35.3-28.7 64-64 64s-64-28.7-64-64s28.7-64 64-64s64 28.7 64 64zm128 64c-35.3 0-64-28.7-64-64s28.7-64 64-64s64 28.7 64 64s-28.7 64-64 64z"
                :fill="isCompetitor ? 'var(--bs-danger)' : 'var(--bs-body-color)'"
            />
        </svg>
    </div>
</template>

<script setup lang="ts">
// Vue imports
import {} from 'vue'

// Third-party imports

// Component imports

// Project imports
// ---------------------------------------- //

// Props and emits definition
defineProps({
    isCompetitor: { type: Boolean, required: false, default: false },
})
defineEmits([])
// ---------------------------------------- //

// Component-specific code
</script>

<style lang="scss" scoped>
@import 'src/assets/scss/bootstrap_override';

$color-base: $body-color;
$color-competitor: $danger;

.icon-container {
    --color-mix-base-to-competitor: #{mix($color-base, $color-competitor, 25%)};
    --color-mix-competitor-to-base: #{mix($color-base, $color-competitor, 35%)};

    height: 1rem;
    width: 1rem;

    & svg path {
        transition: fill 0.2s ease-out;
    }

    &:hover svg path {
        fill: v-bind('isCompetitor ? "var(--color-mix-competitor-to-base)" : "var(--color-mix-base-to-competitor)"');
    }

    &.fs-5 {
        height: 1.25rem;
        width: 1.25rem;
    }

    &.fs-4 {
        height: 1.5rem;
        width: 1.5rem;
    }

    &.fs-3 {
        height: 1.75rem;
        width: 1.75rem;
    }

    &.fs-2 {
        height: 2rem;
        width: 2rem;
    }

    &.fs-1 {
        height: 2.5rem;
        width: 2.5rem;
    }
}
</style>

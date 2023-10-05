<template>
    <div class="d-inline">
        <small class="text-secondary"> ({{ similarity }}%) </small>
        <i class="bi-robot text-secondary"></i>
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
    similarity: { type: Number, required: true },
})
defineEmits([])
// ---------------------------------------- //

// Component-specific code
</script>

<style lang="scss" scoped></style>

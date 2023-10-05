<template>
    <li class="nav-item">
        <router-link :to="link" :class="{ active: isActive }" class="nav-link">
            {{ text }}
        </router-link>
    </li>
</template>

<script setup lang="ts">
// Vue imports
import type { PropType } from 'vue'
import { computed } from 'vue'

// Third-party imports
import { useRoute } from 'vue-router'

// Component imports

// Project imports
// ---------------------------------------- //

// Props and emits definition
const props = defineProps({
    link: { type: Object as PropType<{ name: string }>, required: true },
    text: { type: String, required: true },
})
defineEmits([])
// ---------------------------------------- //

// Component-specific code
const route = useRoute()

const isActive = computed(() => route.name === props.link.name)
</script>

<style lang="scss" scoped></style>

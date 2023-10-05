<template>
    <div :class="{ 'pe-2': scrollIsShown }" class="virtual-list-container" v-bind="containerProps">
        <div v-bind="wrapperProps">
            <div v-for="{ data: item, index } in list" :key="index" :style="{ marginBottom: `${itemMarginBottom}px` }">
                <slot :item="item"></slot>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
// Vue imports
import type { PropType } from 'vue'
import { computed } from 'vue'

// Third-party imports
import { useInfiniteScroll, useThrottleFn, useVirtualList } from '@vueuse/core'

// Component imports

// Project imports
import { useElementDistanceToBottom } from '../../hooks/useElementDistanceToBottom'

// ---------------------------------------- //

// Props and emits definition
const props = defineProps({
    items: { type: Array as PropType<any[]>, required: true },
    itemHeight: { type: Number, required: true },
})
const emit = defineEmits(['reachBottom'])
// ---------------------------------------- //

// Component-specific code
const itemMarginBottom = 16 * 0.75 // 0.75rem
const itemTotalHeight = props.itemHeight + itemMarginBottom
const { list, containerProps, wrapperProps } = useVirtualList(
    computed(() => props.items),
    {
        itemHeight: itemTotalHeight,
        overscan: 4,
    }
)
const containerHeight = useElementDistanceToBottom(containerProps.ref)
const scrollIsShown = computed(() => props.itemHeight * list.value.length > containerHeight.value)

useInfiniteScroll(
    containerProps.ref,
    useThrottleFn(() => emit('reachBottom'), 500),
    { distance: props.itemHeight * 2 }
)
</script>

<style lang="scss" scoped>
@import 'src/assets/scss/mixins';

.virtual-list-container {
    @include scrollbar;

    height: v-bind('`${containerHeight}px`');
}
</style>

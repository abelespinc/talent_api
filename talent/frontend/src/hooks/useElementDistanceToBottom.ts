import { useWindowSize } from '@vueuse/core'
import type { Ref } from 'vue'
import { computed } from 'vue'

export const useElementDistanceToBottom = (elementRef: Ref<HTMLElement | null>) => {
    const { height: windowHeight } = useWindowSize()

    return computed(() => {
        if (elementRef.value) {
            // Window height - element top - body padding bottom
            return windowHeight.value - elementRef.value.getBoundingClientRect().top - 16 * 0.75
        }

        return 100
    })
}

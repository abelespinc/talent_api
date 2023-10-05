<template>
    <span ref="badgeEl" class="badge text-bg-danger" @hover="onBadgeHover()">{{ $t('companies.competitor') }}</span>
</template>

<script setup lang="ts">
// Vue imports
import { ref } from 'vue'

// Third-party imports
import { Tooltip } from 'bootstrap'
import { watchOnce } from '@vueuse/shared'
import { useI18n } from 'vue-i18n'

// Component imports

// Project imports
// ---------------------------------------- //

// Props and emits definition
// defineProps({})
defineEmits([])
// ---------------------------------------- //

// Component-specific code
const { t } = useI18n()

const badgeEl = ref<HTMLElement | null>(null)
let tooltip: Tooltip | undefined

const onBadgeHover = () => {
    tooltip?.show()
}

watchOnce(badgeEl, () => {
    tooltip = new Tooltip(badgeEl.value as HTMLElement, {
        delay: { show: 200, hide: 0 },
        title: t('companies.publishedByCompetitor'),
    })
})
</script>

<style lang="scss" scoped></style>

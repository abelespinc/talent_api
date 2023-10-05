<template>
    <div v-if="showApp" :key="appKey">
        <HeaderMenu></HeaderMenu>

        <main>
            <ContainerLayout>
                <Suspense>
                    <RouterView></RouterView>
                </Suspense>
            </ContainerLayout>
        </main>
    </div>
</template>

<script setup lang="ts">
// Vue imports
import { computed, ref } from 'vue'

// Third-party imports
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'

// Component imports
import HeaderMenu from './components/core/header/HeaderMenu.vue'
import ContainerLayout from './layouts/ContainerLayout.vue'
import { useUserStore } from './stores/userStore'

// Project imports
// ---------------------------------------- //

// Props and emits definition
// defineProps({})
defineEmits([])
// ---------------------------------------- //

// Component-specific code
const router = useRouter()
const userStore = useUserStore()
const { locale } = useI18n({ useScope: 'global' })
const showApp = ref(false)

// Forces a global re render when locale is changed
const appKey = computed(() => `app-${locale.value}`)

// Show the app only when we have the user info
router.isReady().then(() => {
    userStore.isReady().then(() => {
        showApp.value = true
    })
})
</script>

<style lang="scss" scoped></style>

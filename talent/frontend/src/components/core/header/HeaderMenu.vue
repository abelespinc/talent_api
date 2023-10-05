<template>
    <header class="mb-2 mb-xxl-3">
        <div class="container d-flex justify-content-between align-items-center">
            <nav class="navbar navbar-expand-md">
                <div class="container-fluid">
                    <router-link :to="{ name: 'home' }" class="navbar-brand">
                        <img
                            src="https://www.thetalent.club/wp-content/uploads/2020/10/TTC_Mark_Navy.svg"
                            height="50"
                            class="me-4"
                        />
                    </router-link>

                    <button
                        class="navbar-toggler"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#navbarContent"
                        aria-controls="navbarContent"
                        aria-expanded="false"
                        aria-label="Toggle navigation"
                    >
                        <span class="navbar-toggler-icon"></span>
                    </button>

                    <div v-if="showMenuContent" id="navbarContent" class="collapse navbar-collapse">
                        <ul class="navbar-nav me-auto">
                            <HeaderMenuItem
                                v-for="item in menuItemsToShow"
                                :key="item.text"
                                :link="item.link"
                                :text="item.text"
                            >
                            </HeaderMenuItem>
                        </ul>
                    </div>
                </div>
            </nav>

            <div class="d-flex align-items-center gap-3 py-2">
                <LanguageSelect class="py-4"></LanguageSelect>
                <template v-if="userStore.user">
                    |
                    <router-link :to="{ name: 'login' }" class="fw-bold text-danger">
                        {{ $t('users.logOut') }}
                    </router-link>
                </template>
            </div>
        </div>
    </header>
</template>

<script setup lang="ts">
// Vue imports
import { computed } from 'vue'

// Third-party imports
import { useI18n } from 'vue-i18n'

// Component imports
import HeaderMenuItem from './HeaderMenuItem.vue'
import LanguageSelect from '../LanguageSelect.vue'
import { useUserStore } from '../../../stores/userStore'

// Project imports
// ---------------------------------------- //

// Props and emits definition
// defineProps({})
defineEmits([])
// ---------------------------------------- //

// Component-specific code
const { t } = useI18n()
const userStore = useUserStore()
const showMenuContent = computed(() => !!userStore.user)

const menuItems = [
    { link: { name: 'offers' }, text: t('header.offers') },
    { link: { name: 'companies' }, text: t('header.companies') },
    { link: { name: 'configuration' }, text: t('header.configuration'), superUserOnly: true },
]
const menuItemsToShow = computed(() =>
    menuItems.filter((menuItem) => !menuItem.superUserOnly || userStore.user?.isSuperuser)
)
</script>

<style lang="scss" scoped></style>

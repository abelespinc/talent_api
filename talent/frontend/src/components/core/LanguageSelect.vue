<template>
    <div class="position-relative">
        <div class="cursor-pointer" @click="showLanguageDropdown = !showLanguageDropdown">
            <span>{{ getLocaleVerboseName(locale) }}</span>
            <i class="bi-globe ms-2"></i>
        </div>

        <div
            ref="languageDropdown"
            class="language-dropdown position-absolute bg-white shadow-sm px-4 py-2 rounded-1"
            :aria-hidden="!showLanguageDropdown"
            :class="{ visible: showLanguageDropdown }"
        >
            <div
                v-for="availableLocale in locales"
                :key="availableLocale.code"
                class="py-2 mx-n2 rounded-1 cursor-pointer"
            >
                <span @click="setLocale(availableLocale.code)">{{ availableLocale.name }}</span>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
// Vue imports
import { onClickOutside } from '@vueuse/core'
import { computed, ref } from 'vue'

// Third-party imports
import { useI18n } from 'vue-i18n'

// Component imports

// Project imports
import { capitalize } from '../../utils/capitalize'
// ---------------------------------------- //

// Props and emits definition
// const props = defineProps({})
defineEmits([])
// ---------------------------------------- //

// Component-specific code
const { locale, availableLocales } = useI18n()
const languageDropdown = ref(null)
const showLanguageDropdown = ref(false)

const setLocale = (langCode: string) => {
    locale.value = langCode
    // emit('change', langCode)

    // Only change language in backend if user is logged in
    // if (userStore.state.uuid) {
    // changeUserLanguage(langCode).then(() => userStore.fetchMe.bind(userStore))
    // }
}
const getLocaleVerboseName = (loc: string) =>
    capitalize(new Intl.DisplayNames([locale.value], { type: 'language' }).of(loc) || 'Language')

const locales = computed(() =>
    availableLocales
        .filter((loc) => loc !== locale.value)
        .map((loc) => ({
            code: loc,
            name: getLocaleVerboseName(loc),
        }))
)

onClickOutside(languageDropdown, () => {
    showLanguageDropdown.value = false
})
</script>

<style lang="scss" scoped>
.language-dropdown {
    transition: ease-out all 0.2s;
    transform: translateY(-50%) scaleY(0);
    z-index: 1000; // Bootstrap fixed dropdown

    &.visible {
        transform: translateY(0) scaleY(1);
    }
}
</style>

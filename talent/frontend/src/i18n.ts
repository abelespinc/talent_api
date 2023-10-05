import { createI18n } from 'vue-i18n'
import es from './locales/es.json'
import en from './locales/en.json'
import fr from './locales/fr.json'
import nl from './locales/nl.json'

type MessageSchema = typeof es
type Locales = 'es' | 'en' | 'fr' | 'nl'

const defaultLocale = 'es'
const locales = ['es', 'en', 'fr', 'nl']

export const i18n = createI18n<[MessageSchema], Locales>({
    legacy: false,
    locale: (import.meta.env.VITE_I18N_LOCALE as string) || defaultLocale,
    fallbackLocale: (import.meta.env.VITE_I18N_FALLBACK_LOCALE as string) || defaultLocale,
    messages: { es, en, fr, nl },
    silentFallbackWarn: true,
})

const parsedNavigatorLanguage = (): Locales => {
    const navigatorLanguage = navigator.language
    const subCode = navigatorLanguage.split('-')[0]

    if (locales.includes(subCode)) {
        return subCode as Locales
    }

    return defaultLocale
}

i18n.global.locale.value = parsedNavigatorLanguage()

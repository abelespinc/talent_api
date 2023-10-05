module.exports = {
    productionSourceMap: !import.meta.env.PROD,

    pluginOptions: {
        i18n: {
            locale: 'es',
            fallbackLocale: 'es',
            localeDir: 'locales',
            enableLegacy: false,
            runtimeOnly: true,
            compositionOnly: true,
            fullInstall: false,
        },
    },
}

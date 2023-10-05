module.exports = {
    extends: ['@antfu/ts', '@antfu/vue', 'prettier'],
    rules: {
        // Common
        curly: ['error', 'all'], // eslint-disable-line quote-props
        'arrow-parens': ['error', 'always'],

        // https://eslint.vuejs.org/rules/html-self-closing.html
        'vue/html-self-closing': ['off'],
        // https://eslint.vuejs.org/rules/component-tags-order.html
        'vue/component-tags-order': ['error', { order: ['template', 'script', 'style'] }],
        // https://eslint.vuejs.org/rules/require-prop-types.html
        'vue/require-prop-types': 'error',
        // https://eslint.vuejs.org/rules/require-default-prop.html
        'vue/require-default-prop': 'error',
        // https://eslint.vuejs.org/rules/v-on-event-hyphenation.html
        'vue/v-on-event-hyphenation': ['warn', 'always', { autofix: true }],

        // Import order
        // https://github.com/import-js/eslint-plugin-import/blob/v2.26.0/docs/rules/order.md
        'import/order': [
            'error',
            {
                groups: ['builtin', 'external', ['internal', 'parent', 'sibling', 'index']],
            },
        ],
    },
    settings: {
        // https://eslint-plugin-vue-i18n.intlify.dev/started.html#usage
        'vue-i18n': {
            localeDir: './src/locales/*.json',
            messageSyntaxVersion: '^9.2.2',
        },
    },
}

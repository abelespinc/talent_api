import path from 'node:path'
import { defineConfig, splitVendorChunkPlugin } from 'vite'
import vue from '@vitejs/plugin-vue'
import VueI18nPlugin from '@intlify/unplugin-vue-i18n/vite'
import viteCompression from 'vite-plugin-compression'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        vue({
            script: {
                defineModel: true,
            },
        }),
        VueI18nPlugin({ include: path.resolve(__dirname, './src/locales/*.json') }),
        viteCompression({ ext: '.gz', algorithm: 'gzip' }),
        viteCompression({ ext: '.br', algorithm: 'brotliCompress' }),
        splitVendorChunkPlugin(),
    ],
    logLevel: 'warn',
    envDir: 'env/',
})

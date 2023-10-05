import { createApp } from 'vue'

// Styles
import './assets/scss/index.scss'
import 'bootstrap-icons/font/bootstrap-icons.css'

// Third parties
import { createPinia } from 'pinia'
import { autoAnimatePlugin } from '@formkit/auto-animate/vue'
import { router } from './router'
import { i18n } from './i18n'

// App component
import App from './App.vue'

createApp(App).use(router).use(i18n).use(createPinia()).use(autoAnimatePlugin).mount('#app')

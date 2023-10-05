import type { RouteLocationNormalized, RouteLocationRaw, RouteRecordRaw } from 'vue-router'
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/userStore'

interface RouteGuard {
    check: (to: RouteLocationNormalized) => boolean
    getRedirect: () => RouteLocationRaw
}

const routes: RouteRecordRaw[] = [
    { path: '/login', name: 'login', component: () => import('../views/Login.vue') },
    { path: '/companies', name: 'companies', component: () => import('../views/Companies.vue') },
    { path: '/offers', name: 'offers', component: () => import('../views/Offers.vue') },
    { path: '/recent-searches', name: 'recentSearches', component: () => import('../views/RecentSearches.vue') },
    { path: '/configuration', name: 'configuration', component: () => import('../views/Configuration.vue') },
    { path: '/', name: 'home', redirect: { name: 'offers' } },
]

export const router = createRouter({ history: createWebHistory(import.meta.env.BASE_URL), routes })

const routeGuards: RouteGuard[] = [
    {
        check: (to) => !useUserStore().canRouteTo(to.name),
        getRedirect: () => ({ name: 'login' }),
    },
]

// Check all router guards and redirect if necessary
router.beforeEach(async (to) => {
    let redirectTo!: RouteLocationRaw

    await useUserStore().isReady()

    routeGuards.forEach((routeGuard) => {
        if (!redirectTo && routeGuard.check(to)) {
            redirectTo = routeGuard.getRedirect()
        }
    })

    return redirectTo || true
})

import { defineStore } from 'pinia'
import { removeApiAuthToken, setApiAuthToken } from '../api'
import { getMe, login } from '../api/users'
import { LOGIN_EXEMPT_ROUTES, SUPERUSER_ROUTES } from '../config/routes'
import { AUTH_TOKEN_STORAGE_KEY } from '../config/users'
import type { User } from '../models/users'
import { getCookie, removeCookie, setCookie } from '../utils/cookies'

interface UserStoreState {
    user?: User
}

export const useUserStore = defineStore('user', {
    state: (): UserStoreState => ({
        user: undefined,
    }),

    getters: {},

    actions: {
        isReady() {
            return new Promise<boolean>((resolve) => {
                const authToken = this.getAuthToken()

                if (authToken) {
                    setApiAuthToken(authToken)
                }

                if (this.user) {
                    resolve(true)
                } else if (authToken) {
                    this.getMe()
                        .then(() => resolve(true))
                        .catch(() => resolve(false))
                } else {
                    resolve(false)
                }
            })
        },

        async login(username: string, password: string) {
            const response = await login({ username, password })
            this.setAuthToken(response.token)
            await this.getMe()
        },

        logout() {
            this.removeAuthToken()
            this.$reset()
        },

        async getMe() {
            try {
                this.user = await getMe()
            } catch (error: any) {
                this.logout()
            }
        },

        getAuthToken() {
            return getCookie(AUTH_TOKEN_STORAGE_KEY)
        },

        setAuthToken(authToken: string) {
            setCookie(AUTH_TOKEN_STORAGE_KEY, authToken)
            setApiAuthToken(authToken)
        },

        removeAuthToken() {
            removeCookie(AUTH_TOKEN_STORAGE_KEY)
            removeApiAuthToken()
        },

        canRouteTo(to: string) {
            const userExists = Boolean(this.user)
            const routeIsLoginExempt = LOGIN_EXEMPT_ROUTES.includes(to)
            const routeIsSuperuserOnly = SUPERUSER_ROUTES.includes(to)

            if (routeIsLoginExempt) {
                return true
            }

            if (!userExists) {
                return false
            }

            if (routeIsSuperuserOnly && !this.user?.isSuperuser) {
                return false
            }

            return true
        },
    },
})

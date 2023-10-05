<template>
    <div class="card mx-auto mt-5">
        <div class="card-body p-5">
            <form @submit.prevent="onLoginFormSubmit()">
                <div class="form-floating mb-3">
                    <input
                        id="usernameInput"
                        v-model="username"
                        type="text"
                        class="form-control"
                        :placeholder="$t('users.user')"
                        required
                    />
                    <label for="usernameInput">{{ $t('users.user') }}</label>
                </div>
                <div class="form-floating mb-5">
                    <input
                        id="passwordInput"
                        v-model="password"
                        type="password"
                        class="form-control"
                        :placeholder="$t('users.password')"
                        required
                    />
                    <label for="passwordInput">{{ $t('users.password') }}</label>
                    <small v-if="errors.invalidPassword" class="text-danger fw-semibold">
                        {{ $t('users.login.errors.invalidPassword') }}
                    </small>
                </div>

                <button type="submit" class="btn btn-primary btn-lg d-block w-100">{{ $t('users.signIn') }}</button>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
// Vue imports
import { ref } from 'vue'
import { useRouter } from 'vue-router'

// Third-party imports
import { useUserStore } from '../stores/userStore'

// Component imports

// Project imports

// ---------------------------------------- //

// Props and emits definition
// defineProps({})
defineEmits([])

// ---------------------------------------- //

// Component-specific code
const router = useRouter()
const userStore = useUserStore()
const username = ref()
const password = ref()
const errors = ref({ invalidUsername: false, invalidPassword: false })

const onLoginFormSubmit = () => {
    userStore
        .login(username.value, password.value)
        .then(() => router.push({ name: 'home' }))
        .catch(({ body }) => {
            errors.value.invalidUsername = !!body.username
            errors.value.invalidPassword = !!body.password || !!body.non_field_errors
        })
}

userStore.logout()
</script>

<style lang="scss" scoped>
.card {
    max-width: 500px;
}
</style>

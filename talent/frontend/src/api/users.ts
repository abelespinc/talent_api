import { mande } from 'mande'
import type { CreateUserBody, LoginBody, LoginResponse } from '../models/api/users'
import type { User } from '../models/users'

const users = mande(`${import.meta.env.VITE_BACKEND_URL}/api/users`)

export function getMe() {
    return users.get<User>('/me/')
}

export function login(data: LoginBody) {
    return users.post<LoginResponse>('/login/', data)
}

export function createUser(data: CreateUserBody) {
    return users.post<User>('/register/', data)
}

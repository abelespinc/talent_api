export interface LoginBody {
    username: string
    password: string
}

export interface LoginResponse {
    token: string
}

export interface CreateUserBody {
    username: string
    password: string
}

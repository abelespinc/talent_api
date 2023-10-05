interface BaseQueryState<T> {
    isLoading: boolean
    data: T[]
    moreDataAvailable: boolean
    params: Record<string, any>
    totalCount?: number
}

interface SuccessQueryState<T> extends BaseQueryState<T> {
    isError: false
    isSuccess: true
    error: undefined
}

interface ErrorQueryState<T> extends BaseQueryState<T> {
    isError: true
    isSuccess: false
    error: string
}

interface InitialQueryState<T> extends BaseQueryState<T> {
    isError: false
    isSuccess: false
    error: undefined
}

interface QueryParams {
    limit: number
    offset: number
}

type QueryResponse<T> = Promise<PaginatedResponse<T>>

export type QueryState<T> = SuccessQueryState<T> | ErrorQueryState<T> | InitialQueryState<T>
export type Query<T> = (args: QueryParams) => QueryResponse<T>

export interface PaginatedResponse<T> {
    count: number
    next: string
    previous: string
    results: T[]
}

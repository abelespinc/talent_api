import { reactive, toRefs } from 'vue'

import type { Query, QueryState } from '../models/paginatedQuery'

const INITIAL_LIMIT = 100
const INITIAL_OFFSET = 0

const INITIAL_QUERY_STATE = {
    isLoading: false,
    isError: false,
    isSuccess: false,
    moreDataAvailable: true,
    data: [],
    error: undefined,
    totalCount: undefined,
    params: {
        limit: INITIAL_LIMIT,
        offset: INITIAL_OFFSET,
    },
}

export function usePaginatedQuery<T>(query: Query<T>, params: Record<string, any> = {}) {
    const queryState = reactive<QueryState<T>>({
        ...structuredClone(INITIAL_QUERY_STATE),
        params: { limit: INITIAL_LIMIT, offset: INITIAL_OFFSET, ...params },
    }) as QueryState<T>

    const fetchNextPage = (reset = false) => {
        queryState.isLoading = true

        if (reset) {
            queryState.params.offset = params.offset || 0
        }

        return query(queryState.params)
            .then((response) => {
                if (reset) {
                    // Reset data after fetching values to avoid weird looking animations
                    queryState.data.length = 0
                }

                queryState.isSuccess = true
                queryState.data.push(...response.results)
                queryState.moreDataAvailable = !!response.next
                queryState.totalCount = response.count

                if (response.next) {
                    const queryOffset = Number.parseInt(new URL(response.next).searchParams.get('offset') as string)
                    queryState.params.offset = queryOffset || queryState.params.offset
                }

                return Promise.resolve(response)
            })
            .catch((error: string) => {
                queryState.isError = true
                queryState.error = error

                return Promise.reject(error)
            })
            .finally(() => {
                queryState.isLoading = false
            })
    }

    const fetchAllPages = (perPageCallback?: (results: T[]) => void) => {
        return new Promise<T[]>((resolve) => {
            const getNextPage = () => {
                fetchNextPage().then((response) => {
                    perPageCallback?.(response.results)

                    if (response.next) {
                        getNextPage()
                    } else {
                        resolve(queryState.data)
                    }
                })
            }

            getNextPage()
        })
    }

    return { ...toRefs(queryState), fetchNextPage, fetchAllPages }
}

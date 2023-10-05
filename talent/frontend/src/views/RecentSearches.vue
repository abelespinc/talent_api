<template>
    <div v-if="recentSearches.length" class="d-flex flex-column align-items-center gap-3">
        <div
            v-for="({ search, date }, i) in recentSearches"
            :key="i"
            class="card cursor-pointer"
            @click="onRecentSearchClick(search)"
        >
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <div class="d-flex flex-column mb-2">
                            <span class="fw-bold fs-5">{{ search.job }}</span>
                            <div>
                                <i class="bi-geo-alt-fill me-2"></i>
                                <span>{{ search.location || 'Mundial' }}</span>
                            </div>
                        </div>

                        <small class="fw-semibold">
                            {{ t('recentSearches.performedOn') }} {{ date.toLocaleDateString() }}
                        </small>
                    </div>

                    <i class="bi-arrow-right-circle fs-3"></i>
                </div>
            </div>
        </div>
    </div>

    <div v-else class="text-center mt-5">
        <span class="fw-semibold fs-4">{{ t('recentSearches.empty') }}</span>
    </div>
</template>

<script setup lang="ts">
// Vue imports
import { useLocalStorage } from '@vueuse/core'
import { computed } from 'vue'

// Third-party imports
import { useI18n } from 'vue-i18n'

// Component imports

// Project imports
import { useRouter } from 'vue-router'
import { useOffersStore } from '../stores/offersStore'
import type { OffersSearch, RecentSearch } from '../models/searches'
import { RECENT_SEARCH_STORAGE_KEY } from '../utils/searches'
// ---------------------------------------- //

// Props and emits definition
// defineProps({})
defineEmits([])
// ---------------------------------------- //

// Component-specific code
const { t } = useI18n()

const router = useRouter()
const offersStore = await useOffersStore()
const recentSearches = computed<RecentSearch[]>(() =>
    JSON.parse(useLocalStorage(RECENT_SEARCH_STORAGE_KEY, '[]').value)
        .map((search) => ({
            ...search,
            date: new Date(search.date),
        }))
        .sort((a, b) => b.date.valueOf() - a.date.valueOf())
)

const onRecentSearchClick = (search: OffersSearch) => {
    offersStore.restoreSearch(search)
    router.push({ name: 'offers' })
}
</script>

<style lang="scss" scoped>
@import 'src/assets/scss/mixins';

.card {
    width: 100%;
    max-width: 600px;

    .bi-arrow-right-circle {
        transition: color 0.2s ease-out;
    }

    &:hover .bi-arrow-right-circle {
        color: var(--bs-secondary);
    }
}
</style>

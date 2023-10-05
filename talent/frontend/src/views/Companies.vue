<template>
    <div>
        <div class="pb-4 mb-4 border-bottom border-2">
            <h1 class="fw-bold mb-3">{{ $t('companies.companiesList') }}</h1>

            <div class="d-flex align-items-center justify-content-between flex-wrap gap-4">
                <div class="fw-semibold p-2 px-3 border-start border-2 border-danger">
                    <span>{{ $t('companies.redCompaniesAreCompetitors') }}</span>
                    <br />
                    <span>{{ $t('companies.clickOnIconToMarkAsCompetitor') }}</span>
                </div>

                <div class="bg-white rounded-3 py-3 px-4 shadow-sm">
                    <input v-model="companySearch" type="text" class="border-0" placeholder="Buscar..." />
                    <i class="bi-search ms-2"></i>
                </div>
            </div>
        </div>

        <VirtualInfiniteList v-slot="{ item }" :items="companies" :item-height="226" @reach-bottom="onReachBottom()">
            <CompanyCard
                :company="item"
                class="mx-auto"
                @company-is-competitor-change="onCompanyIsCompetitorChange(item)"
            ></CompanyCard>
        </VirtualInfiniteList>
    </div>
</template>

<script setup lang="ts">
// Vue imports
import { ref } from 'vue'

// Third-party imports

// Component imports
import { watchDebounced } from '@vueuse/shared'
import CompanyCard from '../components/companies/CompanyCard.vue'
import VirtualInfiniteList from '../components/base/VirtualInfiniteList.vue'

// Project imports
import { getCompanies } from '../api/companies'
import type { Company } from '../models/companies'
import { usePaginatedQuery } from '../hooks/usePaginatedQuery'
// ---------------------------------------- //

// Props and emits definition
// defineProps({})
defineEmits([])
// ---------------------------------------- //

// Component-specific code
const COMPANIES_PER_PAGE = 20
const companySearch = ref<string>()

const onCompanyIsCompetitorChange = (company: Company) => {
    company.isCompetitor = !company.isCompetitor
}
const {
    data: companies,
    fetchNextPage: fetchCompanies,
    params,
    moreDataAvailable,
} = usePaginatedQuery(getCompanies, { limit: COMPANIES_PER_PAGE })

const onReachBottom = () => {
    if (moreDataAvailable.value) {
        fetchCompanies()
    }
}

watchDebounced(
    companySearch,
    () => {
        params.value.name = companySearch.value
        fetchCompanies(true)
    },
    { debounce: 250 }
)

fetchCompanies()
</script>

<style lang="scss" scoped>
@import 'src/assets/scss/mixins';

.card {
    width: 100%;
    max-width: 600px;
}

input {
    &:focus-visible {
        outline: none;
    }
}
</style>

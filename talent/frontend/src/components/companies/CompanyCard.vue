<template>
    <div class="card">
        <div class="card-body">
            <div
                class="d-flex justify-content-between align-items-center border-bottom border-opacity-25 border-2 pb-3"
                :class="{ 'text-danger': company.isCompetitor }"
            >
                <div class="d-flex flex-column">
                    <span class="fw-bold fs-5">{{ company.name }}</span>
                    <span>Industria: {{ company.industry || 'desconocida' }}</span>

                    <div>
                        <router-link
                            :to="{ name: 'offers', query: { company: company.name } }"
                            :class="company.isCompetitor ? 'btn-danger' : 'btn-primary'"
                            class="mt-3 btn"
                        >
                            <span v-if="!company.offers">{{ $t('offers.noOffers') }}</span>
                            <span v-else-if="company.offers === 1" class="text-lowercase">
                                {{ company.offers }} {{ $t('offers.offer') }}
                            </span>
                            <span v-else class="text-lowercase">
                                {{ company.offers }} {{ $t('offers.offers', company.offers) }}
                            </span>
                            <i class="bi-arrow-right-circle ms-3"></i>
                        </router-link>
                    </div>
                </div>

                <CompanyCompetitorIcon
                    :is-competitor="company.isCompetitor"
                    class="fs-1 cursor-pointer"
                    @click="onCompetitorIconClick()"
                ></CompanyCompetitorIcon>
            </div>

            <div class="mt-2">
                <span class="fw-semibold fs-5 d-block">{{ $t('companies.profiles') }}</span>
                <div v-if="company.profiles.length" class="d-flex gap-3 align-items-center profiles-container">
                    <a
                        v-for="profile in company.profiles"
                        :key="profile.source"
                        :href="profile.url"
                        target="_blank"
                        class="d-flex align-items-center gap-1"
                    >
                        <span class="text-capitalize fw-semibold">{{ profile.source }}</span>
                        <i class="bi-box-arrow-up-right small"></i>
                    </a>
                </div>
                <span v-else>{{ $t('companies.noProfiles') }}</span>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
// Vue imports
import type { PropType } from 'vue'

// Third-party imports

// Component imports
import CompanyCompetitorIcon from './CompanyCompetitorIcon.vue'

// Project imports
import type { Company } from '../../models/companies'
import { modifyCompany } from '../../api/companies'
// ---------------------------------------- //

// Props and emits definition
const props = defineProps({
    company: { type: Object as PropType<Company>, required: true },
})
const emit = defineEmits(['companyIsCompetitorChange'])
// ---------------------------------------- //

// Component-specific code
const onCompetitorIconClick = () => {
    modifyCompany({ companyId: props.company.id, data: { isCompetitor: !props.company.isCompetitor } }).then(() => {
        emit('companyIsCompetitorChange')
    })
}
</script>

<style lang="scss" scoped>
@import 'src/assets/scss/mixins';

.profiles-container {
    @include scrollbar;

    overflow-x: auto;
    overflow-y: hidden;
}
</style>

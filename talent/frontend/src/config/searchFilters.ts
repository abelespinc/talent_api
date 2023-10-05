import { computed } from 'vue'
import type { OffersSearchFilter } from '../models/offers'
import { i18n } from '../i18n'

const { t } = i18n.global

export const searchFilters = computed<OffersSearchFilter[]>(() => [
    {
        name: 'postingDate',
        options: [
            { text: t('offers.search.filters.postingDate.name'), value: undefined, selected: true, hidden: true },
            { text: t('offers.search.filters.postingDate.today'), value: 'TODAY' },
            { text: t('offers.search.filters.postingDate.yesterday'), value: 'YESTERDAY' },
            { text: t('offers.search.filters.postingDate.last7Days'), value: 'LAST_7_DAYS' },
            { text: t('offers.search.filters.postingDate.last15Days'), value: 'LAST_15_DAYS' },
            { text: t('offers.search.filters.postingDate.last30Days'), value: 'LAST_30_DAYS' },
            { text: t('offers.search.filters.postingDate.last45Days'), value: 'LAST_45_DAYS' },
            { text: t('offers.search.filters.postingDate.last90Days'), value: 'LAST_90_DAYS' },
        ],
    },
    {
        name: 'temporality',
        options: [
            { text: t('offers.search.filters.temporality.name'), value: undefined, selected: true, hidden: true },
            { text: t('offers.search.filters.temporality.fullTime'), value: 'FULL_TIME' },
            { text: t('offers.search.filters.temporality.partTime'), value: 'PART_TIME' },
        ],
    },
    {
        name: 'attendance',
        options: [
            { text: t('offers.search.filters.attendance.name'), value: undefined, selected: true, hidden: true },
            { text: t('offers.search.filters.attendance.onSite'), value: 'ON_SITE' },
            { text: t('offers.search.filters.attendance.remote'), value: 'REMOTE' },
            { text: t('offers.search.filters.attendance.partiallyRemote'), value: 'PARTIALLY_REMOTE' },
        ],
    },
    {
        name: 'contractType',
        options: [
            { text: t('offers.search.filters.contractType.name'), value: undefined, selected: true, hidden: true },
            { text: t('offers.search.filters.contractType.fixed'), value: 'FIXED' },
            { text: t('offers.search.filters.contractType.temporal'), value: 'TEMPORAL' },
            { text: t('offers.search.filters.contractType.internship'), value: 'INTERNSHIP' },
            { text: t('offers.search.filters.contractType.freelance'), value: 'FREELANCE' },
            { text: t('offers.search.filters.contractType.others'), value: 'OTHERS' },
        ],
    },
    {
        name: 'competitor',
        options: [
            { text: t('offers.search.filters.competitor.name'), value: undefined, selected: true, hidden: true },
            { text: t('offers.search.filters.competitor.onlyCompetitors'), value: true },
            { text: t('offers.search.filters.competitor.nonCompetitors'), value: false },
        ],
    },
    {
        name: 'status',
        options: [
            { text: t('offers.search.filters.status.name'), value: undefined, selected: true, hidden: true },
            { text: t('offers.search.filters.status.active'), value: 'ACTIVE' },
            { text: t('offers.search.filters.status.notActive'), value: 'NOT_ACTIVE' },
            { text: t('offers.search.filters.status.noStatus'), value: 'NO_STATUS' },
        ],
    },
    {
        name: 'duplicates',
        options: [
            { text: t('offers.search.filters.duplicates.name'), value: undefined, selected: true, hidden: true },
            { text: t('offers.search.filters.duplicates.withDuplicates'), value: 'YES' },
            { text: t('offers.search.filters.duplicates.withoutDuplicates'), value: 'NO' },
        ],
    },
    {
        name: 'titleAndDescription',
        options: [
            {
                text: t('offers.search.filters.titleAndDescription.name'),
                value: undefined,
                selected: true,
                hidden: true,
            },
            { text: t('offers.search.filters.titleAndDescription.onlyTitle'), value: 'ONLY_TITLE' },
            { text: t('offers.search.filters.titleAndDescription.onlyDescription'), value: 'ONLY_DESCRIPTION' },
        ],
    },
])

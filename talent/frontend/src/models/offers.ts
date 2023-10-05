import type { Company } from './companies'
import type { SelectOption } from './core'

export type OfferInfoType = 'temporality' | 'attendance' | 'contractType' | 'salary'
export type OfferSearchFilters =
    | Extract<OfferInfoType, 'temporality' | 'attendance' | 'contractType'>
    | 'competitor'
    | 'company'
    | 'postingDate'
    | 'minSalary'
    | 'status'
    | 'duplicates'
    | 'titleAndDescription'

export interface Salary {
    min: number
    max: number
    isAi: boolean
}

export interface Offer {
    id: string
    job: string
    url: string
    company: { name: string; isCompetitor: boolean }
    temporality: string
    attendance: string
    contractType: string
    location: string
    postingDate: string
    salary: Salary
    duplicatesCount: number
}

export interface OfferDetailed extends Omit<Offer, 'company' | 'duplicatesCount' | 'location'> {
    offerId: string
    source: string
    company: Company
    recruiter: string
    industry: string
    location: { name: string; hasStandardLocation: boolean }
    educationLevel: string
    experienceLevel: string
    skills: string[]
    description: string
    validUntil: string
    duplicates: OfferDetailedDuplicate[]
    similarities: OfferSimilarities
}

export interface OffersSearchFilter {
    name: OfferSearchFilters
    options: SelectOption[]
}

export interface OfferDetailedDuplicate {
    url: string
    source: string
}

export interface OfferSimilarities {
    job: number | null
    description: number | null
    contractType: number | null
    temporality: number | null
    location: number | null
    attendance: number | null
}

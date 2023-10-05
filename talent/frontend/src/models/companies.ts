export interface Company {
    id: string
    name: string
    isCompetitor: boolean
    offers: number
    industry: string
    profiles: { source: string; url: string }[]
}

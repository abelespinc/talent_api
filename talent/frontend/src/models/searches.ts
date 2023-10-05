export interface OffersSearch {
    job: string
    location: string
    attendance: string
    temporality: string
    contractType: string
    competitor: boolean
    company: string
    postingDate: string
    minSalary: number
    status: string
}

export interface RecentSearch {
    date: string // ISO string
    search: OffersSearch
}

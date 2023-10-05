import type { PaginatedQueryParams } from '.'
import type { Company } from '../companies'

export interface GetCompaniesBody extends PaginatedQueryParams {
    name?: string
    onlyCompetitors?: boolean
}

export interface ModifyCompanyBody {
    companyId: string
    data: Partial<Company>
}

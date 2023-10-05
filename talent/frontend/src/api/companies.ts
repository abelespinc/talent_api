import { mande } from 'mande'
import type { GetCompaniesBody, ModifyCompanyBody } from '../models/api/companies'
import type { Company } from '../models/companies'
import type { PaginatedResponse } from '../models/paginatedQuery'
import { prepareObjectForQuery } from '../utils/objects'

const companies = mande(`${import.meta.env.VITE_BACKEND_URL}/api/companies`)

export function getCompanies({
    onlyCompetitors = undefined,
    name = undefined,
    limit = undefined,
    offset = 0,
}: GetCompaniesBody = {}) {
    return companies.get<PaginatedResponse<Company>>('/', {
        query: prepareObjectForQuery({ limit, offset, onlyCompetitors, name }),
    })
}

export function modifyCompany({ companyId, data }: ModifyCompanyBody) {
    return companies.patch<Company>(`${companyId}/`, data)
}

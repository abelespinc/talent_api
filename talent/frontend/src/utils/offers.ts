import type { Salary } from '../models/offers'

const SALARY_LOCALE_OPTIONS = { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }

export function salaryToString(salary: Salary) {
    if (!salary.min && !salary.max) {
        return null
    }

    const min = salary.min ? salary.min.toLocaleString(undefined, SALARY_LOCALE_OPTIONS) : undefined
    const max = salary.max ? salary.max.toLocaleString(undefined, SALARY_LOCALE_OPTIONS) : undefined

    if (min && max) {
        return `${min} - ${max}`
    }

    return min || max
}

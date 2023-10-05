export interface SelectOption {
    text: string
    value?: string | number | boolean
    hidden?: boolean
    disabled?: boolean
    selected?: boolean
}

export interface Configuration {
    statusScrapyEnabled: boolean
    statusScrapyPeriodicity: number
    statusScrapyDaysToStart: number
    statusScrapyDuration: number
    scrapyJobKeywords: string[]
}

export type ScrapyConfiguration = Pick<
    Configuration,
    | 'statusScrapyEnabled'
    | 'statusScrapyDaysToStart'
    | 'statusScrapyDuration'
    | 'statusScrapyPeriodicity'
    | 'scrapyJobKeywords'
>

<template>
    <div v-if="configuration">
        <h1 class="text-danger fw-bold mb-4">WORK IN PROGRESS - NOT WORKING YET</h1>
        <div class="border-bottom border-opacity-25 border-2 pb-3">
            <h3 class="fw-bold">Scrapy</h3>

            <div class="row mb-4">
                <div v-for="field in scrapyConfigurationFields" :key="field" class="col-md-4">
                    <div class="form-floating">
                        <input
                            :id="field"
                            v-model.number="configuration[field]"
                            type="number"
                            class="form-control bg-white"
                            :placeholder="$t(`configuration.scrapy.${field}.name`)"
                        />
                        <label class="fw-semibold" :for="field">
                            {{ $t(`configuration.scrapy.${field}.name`) }}
                        </label>
                    </div>
                    <p class="mb-0 mt-1">{{ $t(`configuration.scrapy.${field}.helpText`) }}</p>
                </div>
            </div>

            <div>
                <h5 class="fw-semibold">Job keywords</h5>
                <div class="row" style="--bs-gutter-x: 0.5rem; --bs-gutter-y: 0.5rem">
                    <div class="col-xxl-3 col-xl-4 col-sm-6">
                        <input
                            v-model="newJobKeyword"
                            type="text"
                            class="form-control bg-white"
                            placeholder="Nueva keyword"
                            @change="onNewJobKeywordChange()"
                        />
                    </div>
                    <div
                        v-for="i in configuration.scrapyJobKeywords.length"
                        :key="i"
                        class="col-xxl-3 col-xl-4 col-sm-6"
                    >
                        <input
                            v-model="configuration.scrapyJobKeywords[i - 1]"
                            type="text"
                            class="form-control bg-white"
                            @change="onJobKeywordChange(i - 1)"
                        />
                    </div>
                </div>
            </div>
        </div>

        <div class="d-flex align-items-center gap-3 mt-4">
            <button
                :class="{
                    'btn-success': saveStatus === 'SUCCESS',
                    'btn-danger': saveStatus === 'ERROR',
                    'btn-primary': !saveStatus,
                }"
                class="btn btn-lg"
                @click="onSaveChanges()"
            >
                {{ $t('saveChanges') }}
            </button>
            <button
                :class="configuration.statusScrapyEnabled ? 'btn-danger' : 'btn-success'"
                type="button"
                class="btn btn-lg"
                @click="onToggleScrapyClick()"
            >
                <template v-if="configuration.statusScrapyEnabled">Parar scrapy</template>
                <template v-else>Iniciar scrapy</template>
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
// Vue imports
import { ref, watch } from 'vue'

// Third-party imports

// Component imports

// Project imports
import { getConfiguration, modifyConfiguration } from '../api/core'
import type { Configuration, ScrapyConfiguration } from '../models/core'
// ---------------------------------------- //

// Props and emits definition
// defineProps({})
defineEmits([])
// ---------------------------------------- //

// Component-specific code
const scrapyConfigurationFields: (keyof ScrapyConfiguration)[] = [
    'statusScrapyPeriodicity',
    'statusScrapyDaysToStart',
    'statusScrapyDuration',
]
const configuration = ref<Configuration>()
const newJobKeyword = ref()
const saveStatus = ref<'SUCCESS' | 'ERROR'>()

const onSaveChanges = () => {
    if (configuration.value) {
        modifyConfiguration({ data: configuration.value })
            .then(() => {
                saveStatus.value = 'SUCCESS'
            })
            .catch(() => {
                saveStatus.value = 'ERROR'
            })
    }
}

const onJobKeywordChange = (keywordIndex: number) => {
    const keyword = configuration.value?.scrapyJobKeywords[keywordIndex]

    if (!keyword && configuration.value) {
        configuration.value.scrapyJobKeywords.splice(keywordIndex, 1)
    }
}

const onNewJobKeywordChange = () => {
    if (newJobKeyword.value) {
        configuration.value?.scrapyJobKeywords.push(newJobKeyword.value)
        newJobKeyword.value = undefined
    }
}

const onToggleScrapyClick = () => {
    if (configuration.value) {
        modifyConfiguration({ data: { statusScrapyEnabled: !configuration.value.statusScrapyEnabled } }).then(() => {
            configuration.value.statusScrapyEnabled = !configuration.value.statusScrapyEnabled
        })
    }
}

getConfiguration().then((response) => {
    configuration.value = response
})

watch(saveStatus, () => {
    setTimeout(() => {
        saveStatus.value = undefined
    }, 2000)
})
</script>

<style lang="scss" scoped>
p {
    font-size: 0.8rem;
    line-height: 1.25;
}
</style>

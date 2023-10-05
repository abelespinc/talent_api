<template>
    <BaseModal v-model:trigger="trigger">
        <template #title>Selecciona una localización</template>
        <template #body>
            <div :class="{ 'mb-4': locations.length }">
                <input v-model="searchText" class="form-control" placeholder="Buscar localización" />
            </div>

            <div v-show="isEmptySearch" class="px-4 pt-5 pb-4 text-center">
                <span class="fw-semibold text-muted">{{ $t('locations.search.badSearch') }}</span>
            </div>

            <h5 v-show="cities.length" class="fw-bold">{{ $t('locations.type.subregion') }}</h5>
            <div class="d-flex flex-column gap-2">
                <div
                    v-for="subregion in subregions"
                    :key="subregion.id"
                    :class="{ 'text-bg-primary': subregion.id === selectedLocation?.id }"
                    class="p-3 rounded rounded-3 border border-primary cursor-pointer location"
                    @click="selectedLocation = subregion"
                >
                    {{ subregion.name }}
                </div>
            </div>

            <hr v-show="cities.length" />

            <h5 v-show="cities.length" class="fw-bold">{{ $t('locations.type.city') }}</h5>
            <div class="d-flex flex-column gap-2">
                <div
                    v-for="city in cities"
                    :key="city.id"
                    :class="{ 'text-bg-primary': city.id === selectedLocation?.id }"
                    class="p-3 rounded rounded-3 border border-primary cursor-pointer location"
                    @click="selectedLocation = city"
                >
                    {{ city.name }}
                </div>
            </div>
        </template>
        <template #footer>
            <div class="d-flex justify-content-between align-items-center w-100">
                <small class="link-muted cursor-pointer fw-semibold" @click="trigger = false">Cancelar</small>

                <span
                    class="fw-semibold"
                    :class="selectedLocation ? 'link-primary cursor-pointer' : 'text-primary opacity-50'"
                    @click="onSave()"
                >
                    Guardar
                </span>
            </div>
        </template>
    </BaseModal>
</template>

<script setup lang="ts">
// Vue imports
import { nextTick, ref, watch } from 'vue'

// Third-party imports
import { useI18n } from 'vue-i18n'

// Component imports
import BaseModal from '../shared/modals/BaseModal.vue'
import type { LocationForSearch, LocationType } from '../../models/locations'
import { useLocationSearch } from '../../hooks/useLocationSearch'

// Project imports

// ---------------------------------------- //

// Props and emits definition
// defineProps({})
defineEmits([])
const trigger = defineModel<boolean>('trigger', { required: true })
const vModel = defineModel<{ id: string; type: LocationType }>()

// i18n translation function
const { t } = useI18n()

// ---------------------------------------- //

// Component-specific code
const searchText = ref('')
const selectedLocation = ref<LocationForSearch>()
const { locations, cities, subregions, isEmptySearch } = useLocationSearch(searchText)

function onSave() {
    if (selectedLocation.value) {
        vModel.value = selectedLocation.value
        trigger.value = false
    }
}

watch(trigger, (_trigger) => {
    nextTick().then(() => {
        if (_trigger) {
            searchText.value = ''
            locations.value = []
            selectedLocation.value = undefined
        }
    })
})
</script>

<style lang="scss" scoped>
.location {
    transition: all 0.2s ease-out;

    &:hover {
        background-color: var(--bs-primary);
        color: white;
    }
}
</style>

<i18n>
{
    "ca": {

    },
    "es": {

    },
    "en": {
        
    }
}
</i18n>

<template>
    <teleport to="body">
        <div ref="modalRef" v-bind="$attrs" class="modal fade">
            <div
                class="modal-dialog"
                :class="{ 'modal-sm': sm, 'modal-lg': lg, 'modal-xl': xl, 'modal-dialog-centered': verticallyCentered }"
            >
                <div class="modal-content" :style="{ backgroundColor }">
                    <div
                        :class="{
                            'border-0': !headerBorder || (!slots.title && !slots.subtitle),
                            'pb-0': !slots.title && !slots.subtitle,
                            [headerClass]: true,
                        }"
                        class="modal-header d-flex justify-content-between align-items-center gap-5"
                    >
                        <div class="flex-grow-1">
                            <h4 class="fw-bold mb-0">
                                <slot name="title"></slot>
                            </h4>
                            <h6 class="text-muted mb-0">
                                <slot name="subtitle"></slot>
                            </h6>
                        </div>
                        <button
                            v-if="!static"
                            type="button"
                            class="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Close"
                            @click="onCloseClick()"
                        ></button>
                    </div>
                    <div class="modal-body" :class="{ 'pt-0': !slots.title && !slots.subtitle }">
                        <slot name="body"></slot>
                    </div>
                    <div v-if="slots.footer" class="modal-footer">
                        <slot name="footer"></slot>
                    </div>
                </div>
            </div>
        </div>
    </teleport>
</template>

<script setup lang="ts">
// Vue imports
import { computed, onUnmounted, ref, useSlots, watch } from 'vue'

// Third-party imports
// import { useI18n } from 'vue-i18n'
import { Modal } from 'bootstrap'
import { watchOnce } from '@vueuse/core'

// Component imports

// Project imports

// ---------------------------------------- //

// Props and emits definition
const props = defineProps({
    trigger: { type: Boolean, required: true },
    headerBorder: { type: Boolean, required: false, default: true },
    headerClass: { type: String, required: false, default: '' },
    sm: { type: Boolean, required: false, default: false },
    lg: { type: Boolean, required: false, default: false },
    xl: { type: Boolean, required: false, default: false },
    verticallyCentered: { type: Boolean, required: false, default: false },
    static: { type: Boolean, required: false, default: false }, // User can't leave the modal until we say it
    backgroundColor: { type: String, required: false, default: '#fff' },
})
const emit = defineEmits(['openModal', 'closeModal', 'showModal', 'hideModal', 'update:trigger'])

// i18n translation function
// const { t } = useI18n()

// ---------------------------------------- //

// Component-specific code
const modalRef = ref<Element>()
const modal = ref<Modal>()
const slots = useSlots()
const computedTrigger = computed<boolean>({
    get() {
        return props.trigger
    },
    set(newValue) {
        if (!props.static) {
            emit('update:trigger', newValue)

            if (newValue) {
                emit('openModal')
            } else {
                emit('closeModal')
                emit('hideModal') // TODO: Deprecate
            }
        }
    },
})

function onCloseClick() {
    modal.value?.hide()
}

onUnmounted(() => {
    modal.value?.dispose()
})

watchOnce(modalRef, () => {
    modal.value = new Modal(modalRef.value as Element, {
        backdrop: props.static ? 'static' : true,
        keyboard: !props.static,
    })
    modalRef.value?.addEventListener('hidden.bs.modal', () => {
        computedTrigger.value = false
    })
    modalRef.value?.addEventListener('shown.bs.modal', () => {
        computedTrigger.value = true
    })

    watch(
        computedTrigger,
        () => {
            if (computedTrigger.value) {
                modal.value?.show()
            } else {
                modal.value?.hide()
            }
        },
        { immediate: true }
    )
})

defineExpose({ modal })
</script>

<script lang="ts">
export default { inheritAttrs: false }
</script>

<style lang="scss" scoped></style>

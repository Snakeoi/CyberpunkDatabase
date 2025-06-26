<script setup>
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'
import { computed } from 'vue'

const props = defineProps({
  notes: {
    type: String,
    default: ''
  },
  isChanged: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:notes', 'save', 'cancel'])

const model = computed({
  get: () => props.notes,
  set: value => emit('update:notes', value)
})
</script>

<template>
  <div>
    <div class="buttons has-addons is-right">
      <button :disabled="!isChanged" class="button is-primary" @click="$emit('save')">
        <i class="icon-save"></i> Zapisz notatki
      </button>
      <button class="button is-warning" :disabled="!isChanged" @click="$emit('cancel')">
        <i class="icon-remove"></i> Anuluj zmiany
      </button>
    </div>
    <QuillEditor
      theme="snow"
      :content-type="'html'"
      :placeholder="'Opis postaci'"
      v-model:content="model"
    />
  </div>
</template>

<style scoped>
</style>

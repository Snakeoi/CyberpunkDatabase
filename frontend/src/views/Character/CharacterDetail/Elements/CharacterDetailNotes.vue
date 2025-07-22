<script setup>

import {QuillEditor} from "@vueup/vue-quill";
import {computed, onMounted, ref} from "vue";

const props = defineProps({
  character: {
    type: Object,
    required: true
  }
});

onMounted(() => {
  characterNotes.value = props.character.notes;
})

const characterNotes = ref('');

const isNotesChanged = computed(() => {
  return characterNotes.value !== props.character.notes;
})

const updateNotes = () => {
  props.character.notes = characterNotes.value;
}
</script>

<template>
<div>
  <div class="buttons has-addons is-right">
    <button :disabled="!isNotesChanged" class="button is-primary" @click="updateNotes">
      <i class="icon-save"></i> Zapisz notatki
    </button>
    <button class="button is-warning" :disabled="!isNotesChanged" @click="characterNotes = character.notes">
      <i class="icon-remove"></i> Anuluj zmiany
    </button>
  </div>

  <QuillEditor
       theme="snow"
       :content-type="'html'"
       :placeholder="'Opis postaci'"
       v-model:content="characterNotes"
  />
</div>
</template>

<style scoped>

</style>
<script setup>

import {sheetModes} from "@/enums.js";
import {ref} from "vue";
import {deleteResource} from "@/assets/utils/axios/crud.js";
import router from "@/router/index.js";
import {useToasterStore} from "@/stores/toaster.js";
import {useRoute} from "vue-router";

const toasterStore = useToasterStore();
const route = useRoute();

const props = defineProps({
  character: {
    type: Object,
    required: true
  },
  sheetMode: {
    type: String,
    default: sheetModes.play
  }
});

const ensureDeletingCharacter = ref('');

const deleteCharacter = async () => {
  if (ensureDeletingCharacter.value !== props.character.name) {
    toasterStore.addMessage('error', 'Proszę wpisać nazwę postaci aby potwierdzić usunięcie.');
  } else {
    await deleteResource(
        `/character/${route.params.id}/`,
        response => {
          router.push({name: 'character-index'});
          toasterStore.addMessage('success', `Postać ${props.character.name} została usunięta.`);
        },
        error => {
          toasterStore.bulkRegisterBackendErrors(error);
        }
    );
  }
}
</script>

<template>
<div class="box" v-if="sheetMode === sheetModes.deleting">
  <div class="field has-addons">
    <div class="control">
      <input class="input"
         type="text"
         placeholder="Wpisz nazwę postaci"
         :class="{'is-danger': ensureDeletingCharacter === character.name}"
         @keyup.enter="deleteCharacter()"
         v-model="ensureDeletingCharacter"/>
    </div>
    <div class="control">
      <button class="button is-danger"
              :disabled="ensureDeletingCharacter !== character.name"
              @click="deleteCharacter">
        <i class="icon-trash mr-3"></i> Usuń postać
      </button>
    </div>
  </div>
</div>
</template>

<style scoped>

</style>
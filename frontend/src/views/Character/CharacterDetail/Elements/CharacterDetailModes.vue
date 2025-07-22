<script setup>

import {sheetModes} from "@/enums.js";
import {useRoute} from "vue-router";

const route = useRoute();

const model = defineModel({
  type: String,
  default: sheetModes.play
});
</script>

<template>
<div class="field is-grouped is-grouped-right">
  <div class="control">
    <div class="buttons has-addons is-centered">
      <button class="button"
              v-if="route.params.id"
              @click="model = sheetModes.play"
              :class="{'is-primary': model === sheetModes.play}">
        <i class="icon-user mr-3"></i>Gra</button>
      <button class="button"
              v-if="route.params.id"
              @click="model = sheetModes.edit"
              :class="{'is-warning': model === sheetModes.edit}">
        <i class="icon-edit mr-3"></i>Edycja</button>
      <button class="button"
              v-if="route.params.id"
              @click="model = sheetModes.deleting"
              :class="{'is-danger': model === sheetModes.deleting}">
        <i class="icon-trash mr-3"></i>Usuwanie</button>
      <RouterLink :to="{name: 'character-print', id: route.params.id}" class="button">
        <i class="icon-print mr-3"></i>Drukuj
      </RouterLink>
    </div>
  </div>
</div>
</template>

<style scoped>

</style>
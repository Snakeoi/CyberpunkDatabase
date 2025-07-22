<script setup>

import {sheetModes} from "@/enums.js";
import Input from "@/components/form/Input.vue";

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
</script>

<template>
<Input v-if="sheetMode === sheetModes.edit" class="is-large mb-4" v-model="character.name"/>
    <h1 v-else class="title is-1">{{ character.name }}</h1>
</template>

<style scoped>

</style>
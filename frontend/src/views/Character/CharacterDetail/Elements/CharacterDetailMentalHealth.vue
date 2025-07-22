<script setup>

import Ability from "@/components/character/Ability.vue";
import Abilities from "@/components/character/Abilities.vue";

const props = defineProps({
  character: {
    type: Object,
    required: true
  },
  sheetMode: {
    type: String,
    default: 'play'
  }
});
</script>

<template>
<h2 class="title is-4">Psychika</h2>
<Abilities>
  <Ability v-model="character.humanity" :editableAt="['play', 'edit']" :sheetMode=sheetMode heading="Człowieczeństwo"/>
  <Ability v-model="character.emp_base" class="subtitle" :sheetMode=sheetMode heading="EMP baza"/>
  <Ability v-model="character.emp_debuff" class="subtitle" :class="{'has-text-danger': character.emp_debuff !== 0}" heading="EMP kara"/>
  <Ability v-model="character.emp" heading="EMP"/>
</Abilities>
</template>

<style scoped>

</style>
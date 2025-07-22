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
<h2 class="title is-4">Zdrowie</h2>
<Abilities>
  <Ability v-model="character.health" :editableAt="['play', 'edit']" :sheetMode="sheetMode" heading="Zdrowie"/>
  <Ability v-model="character.health_base" heading="Max. zdrowie"/>
  <Ability v-model="character.serious_wounds" heading="Poważne rany"/>
  <Ability v-model="character.survivability" heading="Przeżywalność"/>
</Abilities>
</template>

<style scoped>

</style>
<script setup>

import Abilities from "@/components/character/Abilities.vue";
import Ability from "@/components/character/Ability.vue";
import {computed} from "vue";

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

const characterAbilitiesCost = computed(() => {
  return props.character.int + props.character.ref
      + props.character.dex + props.character.tech
      + props.character.cool + props.character.will
      + props.character.luck + props.character.move
      + props.character.body + props.character.emp_base;
});
</script>

<template>
<div class="box">
  <Abilities>
    <Ability v-model="character.int" :sheetMode=sheetMode heading="INT"/>
    <Ability v-model="character.ref" :sheetMode=sheetMode heading="REF"/>
    <Ability v-model="character.dex" :sheetMode=sheetMode heading="ZW"/>
    <Ability v-model="character.tech" :sheetMode=sheetMode heading="TECH"/>
    <Ability v-model="character.cool" :sheetMode=sheetMode heading="CHA"/>
    <Ability v-model="character.will" :sheetMode=sheetMode heading="SW"/>
    <Ability v-model="character.body" :sheetMode=sheetMode heading="BC"/>
    <Ability v-model="character.luck" :sheetMode=sheetMode heading="SZ"/>
    <Ability v-model="character.move" :sheetMode=sheetMode heading="RUCH"/>
  </Abilities>
  <p class="has-text-centered">Koszt zdolności: <b>{{ characterAbilitiesCost }}</b></p>
</div>
</template>

<style scoped>

</style>
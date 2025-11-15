<script setup>

import Abilities from "@/components/character/Abilities.vue";
import Ability from "@/components/character/Ability.vue";
import {computed} from "vue";
import {abilitiesEnum} from "@/enums.js";

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
    <Ability v-model="character.int" :sheetMode=sheetMode :heading="abilitiesEnum.int"/>
    <Ability v-model="character.ref" :sheetMode=sheetMode :heading="abilitiesEnum.ref"/>
    <Ability v-model="character.dex" :sheetMode=sheetMode :heading="abilitiesEnum.dex"/>
    <Ability v-model="character.tech" :sheetMode=sheetMode :heading="abilitiesEnum.tech"/>
    <Ability v-model="character.cool" :sheetMode=sheetMode :heading="abilitiesEnum.cool"/>
    <Ability v-model="character.will" :sheetMode=sheetMode :heading="abilitiesEnum.will"/>
    <Ability v-model="character.body" :sheetMode=sheetMode :heading="abilitiesEnum.body"/>
    <Ability v-model="character.luck" :sheetMode=sheetMode :heading="abilitiesEnum.luck"/>
    <Ability v-model="character.move" :sheetMode=sheetMode :heading="abilitiesEnum.move"/>
  </Abilities>
  <p class="has-text-centered">Koszt zdolności: <b>{{ characterAbilitiesCost }}</b></p>
</div>
</template>

<style scoped>

</style>
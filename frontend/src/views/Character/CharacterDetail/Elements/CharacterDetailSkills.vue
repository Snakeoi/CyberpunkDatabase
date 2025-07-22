<script setup>

import {sheetModes} from "@/enums.js";
import {computed, ref} from "vue";
import {deleteResource, updateResource} from "@/assets/utils/axios/crud.js";
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

const orderedCharacterSkills = computed(() => {
  return props.character.character_skills.sort((a, b) => {
    return a.skill.name.localeCompare(b.skill.name);
  });
});

const summarySkillsCost = computed(() => {
  return props.character.character_skills.reduce((acc, skill) => {
    return acc + (skill.level * skill.skill.cost_multiplier);
  }, 0);
});

const updateCharacterSkill = async (skill, addValue) => {
  const data = {
    level: skill.level + addValue,
  }
  await updateResource(
      `/character/${route.params.id}/skill/${skill.id}/`,
      data,
      response => {
        props.character.character_skills[props.character.character_skills.indexOf(skill)] = response.data;
      },
      error => {
        toasterStore.bulkRegisterBackendErrors(error);
      }
  );
}

const deleteCharacterSkill = async (skill) => {
  await deleteResource(
      `/character/${route.params.id}/skill/${skill.id}/`,
      response => {
        props.character.character_skills.splice(props.character.character_skills.indexOf(skill), 1);
        toasterStore.addMessage('success', `Umiejętność ${skill.skill.name} została usunięta.`);
      },
      error => {
        toasterStore.bulkRegisterBackendErrors(error);
      }
  );
}

</script>

<template>
<h2 class="title is-4">Umiejętności</h2>
<p class="has-text-right">Koszt umiejętności: <b>{{ summarySkillsCost }}</b></p>
<table class="table is-fullwidth">
  <thead>
  <tr>
    <th>Nazwa</th>
    <th>Dziedziczy</th>
    <th>Poziom</th>
    <th>Cecha</th>
    <th>Baza</th>
    <th v-if="[sheetModes.edit, sheetModes.deleting].includes(sheetMode)">Akcje</th>
  </tr>
  </thead>
  <tbody>
  <tr v-for="skill in orderedCharacterSkills">
    <td>
      {{ skill.skill.name }}
      <span v-if="skill.skill.cost_multiplier > 1" class="has-text-warning">
        (x{{ skill.skill.cost_multiplier }})
      </span>
    </td>
    <td>{{ skill.skill.inherit.toUpperCase() }}</td>
    <td>{{ skill.level }}</td>
    <td>{{ skill.ability_level }}</td>
    <td><b>{{ skill.base }}</b></td>
    <td v-if="sheetMode === sheetModes.edit" class="has-text-primary">
      <i @click=updateCharacterSkill(skill,-1) class="icon-minus-square is-clickable pr-4"></i>
      <i @click=updateCharacterSkill(skill,1) class="icon-plus-square is-clickable"></i>
    </td>
    <td v-if="sheetMode === sheetModes.deleting" class="has-text-danger">
      <i @click=deleteCharacterSkill(skill) class="icon-trash is-clickable"></i>
    </td>
  </tr>
  </tbody>
</table>
</template>

<style scoped>

</style>
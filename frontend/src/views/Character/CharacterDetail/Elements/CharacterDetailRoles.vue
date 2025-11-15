<script setup>

import {sheetModesEnum} from "@/enums.js";
import {deleteResource, updateResource} from "@/assets/utils/axios/crud.js";
import {useToasterStore} from "@/stores/toaster.js";
import {useRoute} from "vue-router";
import {computed} from "vue";

const toasterStore = useToasterStore();
const route = useRoute();

const props = defineProps({
  character: {
    type: Object,
    required: true
  },
  sheetMode: {
    type: String,
    default: sheetModesEnum.play
  }
});

const orderedCharacterRoles = computed(() => {
  return props.character.character_roles.sort((a, b) => {
    return a.role.name.localeCompare(b.role.name);
  });
});

const updateCharacterRole = async (role, addValue) => {
  const data = {
    level: role.level + addValue,
  }
  await updateResource(
      `/character/${route.params.id}/role/${role.id}/`,
      data,
      response => {
        props.character.character_roles[props.character.character_roles.indexOf(role)] = response.data;
      },
      error => {
        toasterStore.bulkRegisterBackendErrors(error);
      }
  );
}

const deleteCharacterRole = async (role) => {
  await deleteResource(
      `/character/${route.params.id}/role/${role.id}/`,
      response => {
        props.character.character_roles.splice(props.character.character_roles.indexOf(role), 1);
        toasterStore.addMessage('success', `Rola ${role.role.name} została usunięta.`);
      },
      error => {
        toasterStore.bulkRegisterBackendErrors(error);
      }
  );
}
</script>

<template>
  <h2 class="title is-4">Role</h2>
  <div class="table-container">
  <table class="table is-fullwidth">
    <thead>
    <tr>
      <th>Nazwa</th>
      <th>Zdolność specjalna</th>
      <th>Poziom</th>
      <th v-if="[sheetModesEnum.edit, sheetModesEnum.deleting].includes(sheetMode)">Akcje</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="role in orderedCharacterRoles">
      <td>{{ role.role.name }}</td>
      <td>{{ role.role.special_ability }}</td>
      <td><b>{{ role.level }}</b></td>
      <td v-if="sheetMode === sheetModesEnum.edit">
        <i @click=updateCharacterRole(role,-1) class="icon-minus-square is-size-2 has-text-danger is-clickable pr-4"></i>
        <i @click=updateCharacterRole(role,1) class="icon-plus-square is-size-2 has-text-success is-clickable"></i>
      </td>
      <td v-if="sheetMode === sheetModesEnum.deleting" class="has-text-danger">
        <i @click=deleteCharacterRole(role) class="icon-trash is-size-2 is-clickable"></i>
      </td>
    </tr>
    </tbody>
  </table>
  </div>
</template>

<style scoped>

</style>
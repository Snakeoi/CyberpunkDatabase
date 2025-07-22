<script setup>

import {sheetModes} from "@/enums.js";
import DataTable from "@/components/common/data_table/DataTable.vue";
import SearchInput from "@/components/common/SearchInput.vue";
import {useToasterStore} from "@/stores/toaster.js";
import {useRoute} from "vue-router";
import {createResource, readResource} from "@/assets/utils/axios/crud.js";
import {computed, onMounted, ref} from "vue";

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

const roles = ref([]);
const rolesSerach = ref('')

const getRoles = async () => {
  await readResource(`/role/`, response => {
        roles.value = response.data;
      },
      error => {
        toasterStore.bulkRegisterBackendErrors(error);
      });
}

const filteredRoles = computed(() => {
  const characterCurrentRolesIds = props.character.character_roles.map(role => role.role.id);
  return roles.value.filter(role =>
      role.name.toLowerCase().includes(
          rolesSerach.value.toLowerCase()
      )).filter(role => {
    return !characterCurrentRolesIds.includes(role.id);
  }).sort((a, b) => {
    return a.name.localeCompare(b.name);
  });
})

const addCharacterRole = async (row) => {
  const data = {
    character_id: route.params.id,
    role_id: row.id,
    level: 0,
  }
  await createResource(
      `/character/${route.params.id}/role/`,
      data,
      response => {
       props.character.character_roles.push(response.data);
        toasterStore.addMessage('success', `Rola ${response.data.role.name} została dodana.`);
      },
      error => {
        toasterStore.bulkRegisterBackendErrors(error);
      }
  );
};

onMounted(() => {
  getRoles()
})
</script>

<template>
  <div class="field" v-if="sheetMode === sheetModes.edit">
    <label class="label">Dodaj rolę</label>
    <div class="my-3">
      <SearchInput v-model="rolesSerach"/>
    </div>
    <DataTable
        :storageName="'skills'"
        :data="filteredRoles"
        :onRowClick="addCharacterRole"
        :structure="[
                  {
                    key: 'name',
                    title: 'Nazwa',
                    type: 'string',
                    isSortable: true
                  },
                  {
                    key: 'special_ability',
                    title: 'Zdolność specjalna',
                    type: 'string',
                    isSortable: true
                  },
                ]"
    />
  </div>
</template>

<style scoped>

</style>
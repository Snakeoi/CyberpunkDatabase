<script setup>
import DataTable from '@/components/common/data_table/DataTable.vue'
import SearchInput from '@/components/common/SearchInput.vue'
import { computed } from 'vue'
import { sheetModes } from '@/enums.js'

const props = defineProps({
  orderedRoles: Array,
  filteredRoles: Array,
  rolesSearch: String,
  sheetMode: String,
})

const emit = defineEmits(['update:rolesSearch', 'addRole', 'updateRole', 'deleteRole'])

const searchModel = computed({
  get: () => props.rolesSearch,
  set: value => emit('update:rolesSearch', value)
})
</script>

<template>
  <div class="box">
    <h2 class="title is-4">Role</h2>
    <table class="table is-fullwidth">
      <thead>
      <tr>
        <th>Nazwa</th>
        <th>Zdolność specjalna</th>
        <th>Poziom</th>
        <th v-if="[sheetModes.edit, sheetModes.deleting].includes(sheetMode)">Akcje</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="role in orderedRoles" :key="role.id">
        <td>{{ role.role.name }}</td>
        <td>{{ role.role.special_ability }}</td>
        <td><b>{{ role.level }}</b></td>
        <td v-if="sheetMode === sheetModes.edit" class="has-text-primary">
          <i @click="$emit('updateRole', role, -1)" class="icon-minus-square is-clickable pr-4"></i>
          <i @click="$emit('updateRole', role, 1)" class="icon-plus-square is-clickable"></i>
        </td>
        <td v-if="sheetMode === sheetModes.deleting" class="has-text-danger">
          <i @click="$emit('deleteRole', role)" class="icon-trash is-clickable"></i>
        </td>
      </tr>
      </tbody>
    </table>

    <div class="field" v-if="sheetMode === sheetModes.edit">
      <label class="label">Dodaj rolę</label>
      <div class="my-3">
        <SearchInput v-model="searchModel" />
      </div>
      <DataTable
        :storageName="'skills'"
        :data="filteredRoles"
        :onRowClick="row => $emit('addRole', row)"
        :structure="[
          { key: 'name', title: 'Nazwa', type: 'string', isSortable: true },
          { key: 'special_ability', title: 'Zdolność specjalna', type: 'string', isSortable: true },
        ]"
      />
    </div>
  </div>
</template>

<style scoped>
</style>

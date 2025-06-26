<script setup>
import DataTable from '@/components/common/data_table/DataTable.vue'
import SearchInput from '@/components/common/SearchInput.vue'
import Input from '@/components/form/Input.vue'
import { computed } from 'vue'
import { sheetModes } from '@/enums.js'

const props = defineProps({
  orderedSkills: Array,
  filteredSkills: Array,
  skillsSearch: String,
  newSkillLevel: Number,
  sheetMode: String,
  summaryCost: Number,
})

const emit = defineEmits(['update:skillsSearch', 'update:newSkillLevel', 'addSkill', 'updateSkill', 'deleteSkill'])

const searchModel = computed({
  get: () => props.skillsSearch,
  set: value => emit('update:skillsSearch', value)
})

const levelModel = computed({
  get: () => props.newSkillLevel,
  set: value => emit('update:newSkillLevel', value)
})
</script>

<template>
  <div class="box">
    <h2 class="title is-4">Umiejętności</h2>
    <p class="has-text-right">Koszt umiejętności: <b>{{ summaryCost }}</b></p>
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
      <tr v-for="skill in orderedSkills" :key="skill.id">
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
          <i @click="$emit('updateSkill', skill, -1)" class="icon-minus-square is-clickable pr-4"></i>
          <i @click="$emit('updateSkill', skill, 1)" class="icon-plus-square is-clickable"></i>
        </td>
        <td v-if="sheetMode === sheetModes.deleting" class="has-text-danger">
          <i @click="$emit('deleteSkill', skill)" class="icon-trash is-clickable"></i>
        </td>
      </tr>
      </tbody>
    </table>

    <div class="field" v-if="sheetMode === sheetModes.edit">
      <label class="label">Dodaj umiejętność</label>
      <div class="my-3">
        <div class="field is-grouped">
          <div class="field">
            <label class="label">Szukaj</label>
            <SearchInput v-model="searchModel" />
          </div>
          <div class="field">
            <label class="label">Poziom początkowy</label>
            <Input v-model="levelModel" type="number" min="0" max="10" />
          </div>
        </div>
      </div>
      <DataTable
        :storageName="'skills'"
        :data="filteredSkills"
        :onRowClick="row => $emit('addSkill', row)"
        :structure="[
          { key: 'name', title: 'Nazwa', type: 'string', isSortable: true },
          { key: 'inherit', title: 'Zdolność', type: 'string', isSortable: true },
          { key: 'cost_multiplier', title: 'Mnożnik kosztu', type: 'string', isSortable: true },
        ]"
      />
    </div>
  </div>
</template>

<style scoped>
</style>

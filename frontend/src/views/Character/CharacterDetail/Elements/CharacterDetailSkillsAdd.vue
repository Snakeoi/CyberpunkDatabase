<script setup>

import {sheetModes} from "@/enums.js";
import DataTable from "@/components/common/data_table/DataTable.vue";
import SearchInput from "@/components/common/SearchInput.vue";
import Input from "@/components/form/Input.vue";
import {createResource, readResource} from "@/assets/utils/axios/crud.js";
import {useToasterStore} from "@/stores/toaster.js";
import {useRoute} from "vue-router";
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

const skills = ref([]);

const getSkills = async () => {
  await readResource(`/skill/`, response => {
        skills.value = response.data;
      },
      error => {
        toasterStore.bulkRegisterBackendErrors(error);
      });
}

const skillsSerach = ref('')
const newSkillInitialLevel = ref(0);
const filteredSkills = computed(() => {
  const characterCurrentSkillsIds = props.character.character_skills.map(skill => skill.skill.id);
  return skills.value.filter(skill =>
      skill.name.toLowerCase().includes(
          skillsSerach.value.toLowerCase()
      )).filter(skill => {
    return !characterCurrentSkillsIds.includes(skill.id);
  }).sort((a, b) => {
    return a.name.localeCompare(b.name);
  });
});

const addCharacterSkill = async (row) => {
  const data = {
    character_id: route.params.id,
    skill_id: row.id,
    level: newSkillInitialLevel.value,
  }
  await createResource(
      `/character/${route.params.id}/skill/`,
      data,
      response => {
        props.character.character_skills.push(response.data);
        toasterStore.addMessage('success', `Umiejętność ${response.data.skill.name} (${response.data.level}) została dodana.`);
      },
      error => {
        toasterStore.bulkRegisterBackendErrors(error);
      }
  );
};

onMounted(() => {
  getSkills();
})
</script>

<template>
  <div class="field" v-if="sheetMode === sheetModes.edit">
    <label class="label">Dodaj umiejętność</label>
    <div class="my-3">
      <div class="field is-grouped">
        <div class="field">
          <label class="label">Szukaj</label>
          <SearchInput v-model="skillsSerach"/>
        </div>
        <div class="field">
          <label class="label">Poziom początkowy</label>
          <input class="input" v-model="newSkillInitialLevel" type="number" min="0" max="10"/>
        </div>
      </div>
    </div>
    <DataTable
        :storageName="'skills'"
        :data="filteredSkills"
        :onRowClick="addCharacterSkill"
        :structure="[
                  {
                    key: 'name',
                    title: 'Nazwa',
                    type: 'string',
                    isSortable: true
                  },
                  {
                    key: 'inherit',
                    title: 'Zdolność',
                    type: 'string',
                    isSortable: true
                  },
                  {
                    key: 'cost_multiplier',
                    title: 'Mnożnik kosztu',
                    type: 'string',
                    isSortable: true
                  },
                ]"
    />
  </div>
</template>

<style scoped>

</style>
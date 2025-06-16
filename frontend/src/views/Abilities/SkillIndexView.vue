<script setup>
import {computed, onMounted, ref} from "vue";
import {readResource} from "@/assets/utils/axios/crud.js";
import SearchInput from "@/components/common/SearchInput.vue";
import DataTable from "@/components/common/data_table/DataTable.vue";
import router from "@/router/index.js";
import {adminSettingsViewsStore} from "@/stores/adminSettingsViews.js";
import ConditionalLoader from "@/components/loader/ConditionalLoader.vue";

const isLoading = ref(true);
const skillSettingsViews = adminSettingsViewsStore();
const skills = ref([]);

const filtered = computed(() => {
  return skills.value.filter(skill =>
      skill.name.toLowerCase().includes(
      skillSettingsViews.skillSearchField.toLowerCase()
  ));
})

onMounted(async () => {
  await readResource(
      '/skill/',
      response => {
        skills.value = response.data
      });
  document.title = 'Umiejętności';
  isLoading.value = false;
});

const openDetails = (row) => {
  router.push({name: 'skill-detail', params: {id: row.id}});
}
</script>

<template>
  <ConditionalLoader :is-loading="isLoading">
    <h1 class="title">Umiejętności</h1>
    <div class="field is-grouped is-grouped-right">
      <div class="control">
        <RouterLink class="button is-primary" :to="{name: 'skill-add'}">
          <i class="icon-user-plus mr-3"></i>Dodaj
        </RouterLink>
      </div>
    </div>
    <div class="my-3">
      <SearchInput v-model="skillSettingsViews.skillSearchField"/>
    </div>
    <DataTable
        :storageName="'skills'"
        :data="filtered"
        :onRowClick="openDetails"
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
  </ConditionalLoader>
</template>

<style scoped>

</style>
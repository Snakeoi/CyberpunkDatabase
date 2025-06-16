<script setup>
import {computed, onBeforeMount, onMounted, ref} from "vue";
import {readResource} from "@/assets/utils/axios/crud.js";
import SearchInput from "@/components/common/SearchInput.vue";
import DataTable from "@/components/common/data_table/DataTable.vue";
import router from "@/router/index.js";
import {adminSettingsViewsStore} from "@/stores/adminSettingsViews.js";
import ConditionalLoader from "@/components/loader/ConditionalLoader.vue";

const isLoading = ref(true);
const characterSettingsViews = adminSettingsViewsStore();
const characters = ref([]);

const filtered = computed(() => {
  return characters.value.filter(character =>
      character.name.toLowerCase().includes(
      characterSettingsViews.userSearchField.toLowerCase()
  ))
})

onMounted(async () => {
  await readResource(
      '/character/',
      response => {
        characters.value = response.data
      });
  document.title = 'Postaci';
  isLoading.value = false;
});

const openDetails = (row) => {
  router.push({name: 'character-detail', params: {id: row.id}});
}
</script>

<template>
  <ConditionalLoader :is-loading="isLoading">
    <h1 class="title">Postaci</h1>
    <div class="field is-grouped is-grouped-right">
      <div class="control">
        <div class="buttons has-addons is-centered">
          <RouterLink class="button is-primary" :to="{name: 'character-add'}">
            <i class="icon-user-plus mr-3"></i>Dodaj
          </RouterLink>
          <RouterLink :to="{ name: 'character-generate' }" class="button is-primary">
            <i class="icon-magic mr-3"></i>Generuj
          </RouterLink>
        </div>
      </div>
    </div>
    <div class="my-3">
      <SearchInput v-model="characterSettingsViews.userSearchField"/>
    </div>
    <DataTable
        :storageName="'characters'"
        :data="filtered"
        :onRowClick="openDetails"
        :structure="[
          {
            key: 'name',
            title: 'Name',
            type: 'string',
            isSortable: true
          },
          {
            key: 'roles_list',
            title: 'Role',
            type: 'string',
            isSortable: true,
          }
        ]"
    />
  </ConditionalLoader>
</template>

<style scoped>

</style>
<script setup>
import {createResource, deleteResource, readResource, updateResource} from "@/assets/utils/axios/crud.js";
import {computed, onBeforeMount, ref, watch} from "vue";
import {useRoute} from 'vue-router'
import ConditionalLoader from "@/components/loader/ConditionalLoader.vue";
import {useToasterStore} from "@/stores/toaster.js";
import {sheetModesEnum} from "@/enums.js";
import '@vueup/vue-quill/dist/vue-quill.snow.css';
import CharacterDetailTabs from "@/views/Character/CharacterDetail/Elements/CharacterDetailTabs.vue";
import { io } from "socket.io-client";
import CharacterDetailModes from "@/views/Character/CharacterDetail/Elements/CharacterDetailModes.vue";
import CharacterDetailName from "@/views/Character/CharacterDetail/Elements/CharacterDetailName.vue";
import CharacterDetailDelete from "@/views/Character/CharacterDetail/Elements/CharacterDetailDelete.vue";
import CharacterDetailNotes from "@/views/Character/CharacterDetail/Elements/CharacterDetailNotes.vue";
import CharacterDetailAbilities from "@/views/Character/CharacterDetail/Elements/CharacterDetailAbilities.vue";
import CharacterDetailSkills from "@/views/Character/CharacterDetail/Elements/CharacterDetailSkills.vue";
import CharacterDetailSkillsAdd from "@/views/Character/CharacterDetail/Elements/CharacterDetailSkillsAdd.vue";
import CharacterDetailMentalHealth from "@/views/Character/CharacterDetail/Elements/CharacterDetailMentalHealth.vue";
import CharacterDetailHealth from "@/views/Character/CharacterDetail/Elements/CharacterDetailHealth.vue";
import CharacterDetailRoles from "@/views/Character/CharacterDetail/Elements/CharacterDetailRoles.vue";
import CharacterDetailsRolesAdd from "@/views/Character/CharacterDetail/Elements/CharacterDetailsRolesAdd.vue";
import CharacterDetailBank from "@/views/Character/CharacterDetail/Elements/CharacterDetailBank.vue";

const toasterStore = useToasterStore();

const tabs = ref([
    {
      title: 'Notatki',
      icon: 'icon-sticky-note',

    },
    {
      title: 'Cechy i umiejętności',
      icon: 'icon-calculator',
    },
    {
      title: 'Pieniądze',
      icon: 'icon-money',
    }
]);
const activeTab = ref(tabs.value[1]);


const route = useRoute();
const socket = io();
const isLoading = ref(true);
const character = ref({});
const characterOriginal = ref({});

const sheetMode = ref(sheetModesEnum.play);

const isCharacterChanged = computed(() => {
  return JSON.stringify(character.value) !== JSON.stringify(characterOriginal.value)
})

watch(character, async () => {
  if (isCharacterChanged.value) {
    await updateCharacter();
  }
}, {deep: true});

onBeforeMount(async () => {
  socket.emit('join_character', {character_id: route.params.id})
  socket.on('character_update', data => {
    character.value = data
    characterOriginal.value = {...data}
  });
  await getCharacter()
  document.title = character.value.name
  isLoading.value = false
})

const getCharacter = async () => {
  await readResource(`/character/${route.params.id}/`, response => {
        character.value = response.data;
        characterOriginal.value = {...character.value}
      },
      error => {
        toasterStore.bulkRegisterBackendErrors(error);
      });
}

const updateCharacter = async () => {
  const data = {
    name: character.value.name,
    notes: character.value.notes,
    int: character.value.int,
    ref: character.value.ref,
    dex: character.value.dex,
    tech: character.value.tech,
    cool: character.value.cool,
    will: character.value.will,
    luck: character.value.luck,
    move: character.value.move,
    body: character.value.body,
    humanity: character.value.humanity,
    emp_base: character.value.emp_base,
    health: character.value.health,
  }
  await updateResource(
      `/character/${route.params.id}/`,
      data,
      response => {
        character.value = response.data;
        characterOriginal.value = {...character.value}
      },
      error => {
        toasterStore.bulkRegisterBackendErrors(error);
      }
  );
}

</script>

<template>
  <ConditionalLoader :is-loading="isLoading">

    <div class="buttons is-right">
      <RouterLink :to="{name: 'character-print', id: route.params.id}" class="button">
        <i class="icon-print mr-3" aria-hidden="true"></i>Drukuj
      </RouterLink>
    </div>
    <CharacterDetailName :character="character" :sheetMode="sheetMode"/>
    <CharacterDetailTabs :tabs="tabs" v-model="activeTab"/>


    <div class="content" v-if="activeTab === tabs[0]">
      <CharacterDetailNotes :character="character"/>
    </div>

    <div v-if="activeTab === tabs[1]">
      <CharacterDetailModes v-model="sheetMode"/>
      <CharacterDetailDelete :character="character" :sheetMode="sheetMode"/>
      <CharacterDetailAbilities :character="character" :sheetMode="sheetMode"/>
      <div class="columns">
        <div class="column">
          <div class="box">
            <CharacterDetailMentalHealth :character="character" :sheetMode="sheetMode"/>
          </div>
          <div class="box">
            <CharacterDetailHealth :character="character" :sheetMode="sheetMode"/>
          </div>
          <div class="box">
            <CharacterDetailRoles :character="character" :sheetMode="sheetMode"/>
            <CharacterDetailsRolesAdd :character="character" :sheetMode="sheetMode"/>
          </div>
        </div>
        <div class="column">
          <div class="box">
            <CharacterDetailSkills :character="character" :sheetMode="sheetMode"/>
            <CharacterDetailSkillsAdd :character="character" :sheetMode="sheetMode"/>
          </div>
        </div>
      </div>
    </div>

    <div v-if="activeTab === tabs[2]">
      <CharacterDetailBank/>
    </div>
  </ConditionalLoader>
</template>

<style scoped>

</style>
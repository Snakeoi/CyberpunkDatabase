<script setup>
import {computed, onMounted, ref} from "vue";
import {createResource, deleteResource, readResource, updateResource} from "@/assets/utils/axios/crud.js";
import {useToasterStore} from "@/stores/toaster.js";
import router from "@/router/index.js";

const toasterStore = useToasterStore();

const roles = ref([
    'rocker',
    'solo',
    'netrunner',
    'tech',
    'medic',
    'media',
    'cop',
    'corp',
    'fixer',
    'nomad',
]);

const rolesMap = ref({
    'rocker': 'Rocker',
    'solo': 'Solo',
    'netrunner': 'Netrunner',
    'tech': 'Technik',
    'medic': 'Medyk',
    'media': 'Media',
    'cop': 'Stóż Prawa',
    'corp': 'Korp',
    'fixer': 'Fixer',
    'nomad': 'Nomada',
})

const isGenerating = ref(false);

const selectedRole = ref(roles.value[0]);

onMounted(() => {
  document.title = 'Generuj postać';
});

const generateCharacter = async () => {
  isGenerating.value = true;
  const data = {
    role: selectedRole.value
  }
  await createResource(
    `/character/generate/`,
    data,
    (response) => {
      router.push({name: 'character-detail', params: {id: response.data.character_id}});
      isGenerating.value = false;
    },
    (error) => {
      console.error(error);
      toasterStore.addMessage('error', `Failed to generate character.`);
      isGenerating.value = false;
    }
  );
}
</script>

<template>

  <h1 class="title">Generuj postać</h1>
    <div class="field">
      <label class="label">Wybierz rolę</label>
      <div class="field has-addons">
        <div class="control">
          <div class="select">
            <select v-model="selectedRole">
              <option v-for="role in roles" :key="role" :value="role">{{ rolesMap[role] }}</option>
            </select>
          </div>
        </div>
        <div class="control">
          <button class="button is-primary"
                  :class="{'is-loading': isGenerating}"
                  :disabled="isGenerating"
                  @click="generateCharacter">
            <i class="icon-magic mr-3"></i> Generuj
          </button>
        </div>
      </div>
    </div>

</template>

<style scoped>

</style>
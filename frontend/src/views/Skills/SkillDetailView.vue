<script setup>
import {onBeforeMount, ref, computed} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import Input from '@/components/form/Input.vue';
import ConditionalLoader from '@/components/loader/ConditionalLoader.vue';
import {readResource, updateResource, deleteResource} from '@/assets/utils/axios/crud.js';
import {useToasterStore} from '@/stores/toaster.js';

const toasterStore = useToasterStore();
const route = useRoute();
const router = useRouter();
const isLoading = ref(true);
const showDelete = ref(false);
const ensureDeletingSkill = ref('');
const skill = ref({});
const skillOriginal = ref({});
const patchSchema = ref({});
const abilities = ['int', 'ref', 'dex', 'tech', 'cool', 'will', 'luck', 'move', 'body', 'emp'];

onBeforeMount(async () => {
  await Promise.all([
    readResource('/skill/schema/patch', res => { patchSchema.value = res.data; }),
    readResource(`/skill/${route.params.id}/`, res => {
      skill.value = res.data;
      skillOriginal.value = { ...res.data };
    })
  ]);
  document.title = skill.value.name;
  isLoading.value = false;
});

const isSkillChanged = computed(() => {
  return JSON.stringify(skill.value) !== JSON.stringify(skillOriginal.value);
});

const saveSkill = async () => {
  await updateResource(
    `/skill/${route.params.id}/`,
    skill.value,
    response => {
      skill.value = response.data;
      skillOriginal.value = { ...response.data };
      toasterStore.addMessage('success', `Umiejętność ${response.data.name} została zaktualizowana.`);
    },
    error => {
      toasterStore.bulkRegisterBackendErrors(error);
    }
  );
};

const deleteSkill = async () => {
  if (ensureDeletingSkill.value !== skill.value.name) {
    toasterStore.addMessage('error', 'Proszę wpisać nazwę umiejętności aby potwierdzić usunięcie.');
    return;
  }
  await deleteResource(
    `/skill/${route.params.id}/`,
    () => {
      router.push({ name: 'skill-index' });
      toasterStore.addMessage('success', `Umiejętność ${skill.value.name} została usunięta.`);
    },
    error => {
      toasterStore.bulkRegisterBackendErrors(error);
    }
  );
};
</script>

<template>
  <ConditionalLoader :is-loading="isLoading">
    <div class="field is-grouped is-grouped-right">
      <div class="control">
        <button class="button is-primary" :disabled="!isSkillChanged" @click="saveSkill">
          <i class="icon-save mr-3"></i>Zapisz
        </button>
      </div>
      <div class="control">
        <button class="button is-danger" @click="showDelete = !showDelete">
          <i class="icon-trash mr-3"></i>Usuń
        </button>
      </div>
    </div>
    <Input class="is-large mb-4" v-model="skill.name" :validators="patchSchema?.name?.validators" />
    <div class="field mb-4">
      <label class="label">Dziedziczy</label>
      <div class="select">
        <select v-model="skill.inherit">
          <option v-for="a in abilities" :key="a" :value="a">{{ a.toUpperCase() }}</option>
        </select>
      </div>
    </div>
    <div class="field mb-4">
      <label class="label">Mnożnik kosztu</label>
      <Input type="number" v-model="skill.cost_multiplier" :validators="patchSchema?.cost_multiplier?.validators" />
    </div>
    <div class="box" v-if="showDelete">
      <div class="field has-addons">
        <div class="control">
          <input class="input" type="text" v-model="ensureDeletingSkill" :placeholder="'Wpisz nazwę umiejętności'" />
        </div>
        <div class="control">
          <button class="button is-danger" :disabled="ensureDeletingSkill !== skill.name" @click="deleteSkill">
            <i class="icon-trash mr-3"></i>Usuń
          </button>
        </div>
      </div>
    </div>
  </ConditionalLoader>
</template>

<style scoped>
</style>

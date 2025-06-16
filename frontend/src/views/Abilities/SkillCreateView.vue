<script setup>
import {onBeforeMount, ref} from 'vue';
import Input from '@/components/form/Input.vue';
import ConditionalLoader from '@/components/loader/ConditionalLoader.vue';
import {createResource, readResource} from '@/assets/utils/axios/crud.js';
import router from '@/router/index.js';
import {useToasterStore} from '@/stores/toaster.js';

const toasterStore = useToasterStore();
const isLoading = ref(true);
const skill = ref({
  name: '',
  inherit: 'int',
  cost_multiplier: 1,
});
const postSchema = ref({});
const abilities = ['int', 'ref', 'dex', 'tech', 'cool', 'will', 'luck', 'move', 'body', 'emp'];

onBeforeMount(async () => {
  await readResource('/skill/schema/post', res => {
    postSchema.value = res.data;
  });
  document.title = 'Nowa umiejętność';
  isLoading.value = false;
});

const saveSkill = async () => {
  await createResource(
    '/skill/',
    skill.value,
    response => {
      router.push({name: 'skill-detail', params: {id: response.data.id}});
      toasterStore.addMessage('success', `Umiejętność ${response.data.name} została dodana.`);
    },
    error => {
      toasterStore.bulkRegisterBackendErrors(error);
    }
  );
};
</script>

<template>
  <ConditionalLoader :is-loading="isLoading">
    <h1 class="title">Nowa umiejętność</h1>
    <div class="box">
      <div class="field mb-4">
        <label class="label">Nazwa</label>
        <Input v-model="skill.name" :validators="postSchema?.name?.validators" />
      </div>
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
        <Input type="number" v-model="skill.cost_multiplier" :validators="postSchema?.cost_multiplier?.validators" />
      </div>
      <div class="field is-grouped is-grouped-right">
        <div class="control">
          <button class="button is-primary" @click="saveSkill">
            <i class="icon-save mr-3"></i>Dodaj
          </button>
        </div>
      </div>
    </div>
  </ConditionalLoader>
</template>

<style scoped>
</style>

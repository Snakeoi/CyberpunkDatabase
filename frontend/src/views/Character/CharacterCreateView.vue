<script setup>
import {createResource, readResource} from "@/assets/utils/axios/crud.js";
import {onBeforeMount, ref} from "vue";
import Input from "@/components/form/Input.vue";
import ConditionalLoader from "@/components/loader/ConditionalLoader.vue";
import router from "@/router/index.js";
import {useToasterStore} from "@/stores/toaster.js";

const toasterStore = useToasterStore();

const isLoading = ref(true);

const character = ref({
  name: '',
  notes: '',
  int: 0,
  ref: 0,
  dex: 0,
  tech: 0,
  cool: 0,
  will: 0,
  luck: 0,
  move: 0,
  body: 0,
  emp_base: 0,
  humanity: 0,
});

const postSchema = ref({});

onBeforeMount(async () => {
  await readResource('/character/schema/post', response => {
    postSchema.value = response.data;
  });
  document.title = 'Nowa postać';
  isLoading.value = false;
})

const saveCharacter = async () => {
  await createResource(
    `/character/`,
    character.value,
    (response) => {
      character.value = response.data;
      router.push({name: 'character-detail', params: {id: response.data.id}});
      toasterStore.addMessage('success', `Character ${response.data.name} has been added.`);
    },
    error => {
      toasterStore.bulkRegisterBackendErrors(error);
    });
}
</script>

<template>
  <ConditionalLoader :is-loading="isLoading">

      <div class="field is-horizontal">
        <div class="field-body">
          <div class="field ">
            <div class="field mb-3">
              <label class="label">Ksywa</label>
              <Input
                  v-model="character.name"
                  :validators="postSchema?.name.validators"
              />
            </div>
            <div class="field mb-3">
              <label class="label">Opis</label>
              <Input
                v-model="character.notes"
                type="textarea"
              />
            </div>
            <div class="field is-grouped">
              <div class="field mb-3">
                <label class="label">INT</label>
                <Input
                    v-model="character.int"
                    :validators="postSchema?.int.validators"
                    type="number"
                />
              </div>
              <div class="field mb-3">
                <label class="label">REF</label>
                <Input
                    v-model="character.ref"
                    :validators="postSchema?.ref.validators"
                    type="number"
                />
              </div>
              <div class="field mb-3">
                <label class="label">ZW</label>
                <Input
                    v-model="character.dex"
                    :validators="postSchema?.dex.validators"
                    type="number"
                />
              </div>
              <div class="field mb-3">
                <label class="label">TECH</label>
                <Input
                    v-model="character.tech"
                    :validators="postSchema?.tech.validators"
                    type="number"
                />
              </div>
              <div class="field mb-3">
                <label class="label">CHA</label>
                <Input
                    v-model="character.cool"
                    :validators="postSchema?.cool.validators"
                    type="number"
                />
              </div>
              <div class="field mb-3">
                <label class="label">SW</label>
                <Input
                    v-model="character.will"
                    :validators="postSchema?.will.validators"
                    type="number"
                />
              </div>
              <div class="field mb-3">
                <label class="label">BC</label>
                <Input
                    v-model="character.body"
                    :validators="postSchema?.body.validators"
                    type="number"
                />
              </div>
              <div class="field mb-3">
                <label class="label">SZ</label>
                <Input
                    v-model="character.luck"
                    :validators="postSchema?.luck.validators"
                    type="number"
                />
              </div>
              <div class="field mb-3">
                <label class="label">RUCH</label>
                <Input
                    v-model="character.move"
                    :validators="postSchema?.move.validators"
                    type="number"
                />
              </div>
              <div class="field mb-3">
                <label class="label">EMP BAZA</label>
                <Input
                    v-model="character.emp_base"
                    :validators="postSchema?.emp_base.validators"
                    type="number"
                />
              </div>
              <div class="field mb-3">
                <label class="label">Człowieczeństwo</label>
                <Input
                    v-model="character.humanity"
                    :validators="postSchema?.humanity.validators"
                    type="number"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="field is-grouped is-grouped-right">
        <div class="control">
          <button class="button is-primary" @click="saveCharacter">Dodaj</button>
        </div>
      </div>


  </ConditionalLoader>
</template>

<style scoped>

</style>
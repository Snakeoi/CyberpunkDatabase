<script setup>
import {onMounted, ref} from "vue";
import {createResource, readResource} from "@/assets/utils/axios/crud.js";
import {useRoute} from "vue-router";
import {useToasterStore} from "@/stores/toaster.js";

const route = useRoute();
const toasterStore = useToasterStore();

const entries = ref([]);
const balance = ref(0);
const addNewEntryMode = ref(false);

const getBankEntries = async () => {
  await readResource(`/bank/${route.params.id}`, response => {
    entries.value = response.data;
  }, error => {
    toasterStore.bulkRegisterBackendErrors(error);
  });
};

const getBalance = async () => {
  await readResource(`/bank/${route.params.id}/balance`, response => {
    balance.value = response.data.balance;
  }, error => {
    toasterStore.bulkRegisterBackendErrors(error);
  });
};

const newBankEntryDescription = ref('');
const newBankEntryAmount = ref(0);
const addBankEntry = async () => {
  const entry = {
    character_id: route.params.id,
    description: newBankEntryDescription.value,
    amount: newBankEntryAmount.value
  }
  await createResource(`/bank/`, entry, response => {
    entries.value.unshift(response.data);
    balance.value = balance.value + response.data.amount;
    newBankEntryDescription.value = '';
    newBankEntryAmount.value = 0;
    addNewEntryMode.value = false;
  }, error => {
    toasterStore.bulkRegisterBackendErrors(error);
  });
};

const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp);
  return date.toLocaleDateString('pl-PL', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
};

onMounted(async () => {
  await getBankEntries()
  await getBalance()
});
</script>

<template>
<div class="box is-flex is-justify-content-space-between is-align-items-center">
  <button @click="addNewEntryMode = !addNewEntryMode" class="button" :class="{'is-primary': !addNewEntryMode}">Nowy wpis</button>
  <p><span class="mr-3">Saldo:</span> <span class="is-size-3" :class="{'has-text-danger': balance <= 0}"> {{balance}} eb</span></p>
</div>
<div v-if="addNewEntryMode" class="box">
  <div class="field is-horizontal">
    <div class="field-body">
      <div class="field">
        <label class="label">Opis</label>
        <div class="control">
          <input v-model="newBankEntryDescription" class="input" type="text" placeholder="Opis transakcji">
        </div>
      </div>
      <div class="field">
        <label class="label">Kwota</label>
        <div class="control">
          <input v-model.number="newBankEntryAmount" class="input" type="number" placeholder="Kwota transakcji">
        </div>
      </div>
      <div class="field is-grouped is-grouped-right">
        <div class="control">
          <button @click="addBankEntry" class="button is-primary">Dodaj</button>
        </div>
      </div>
    </div>
  </div>
</div>
<div v-for="entry in entries" :key="entry" class="box">
  <div class="columns is-vcentered">
    <div class="column">
      <p class="is-size-5">{{ formatTimestamp(entry.timestamp) }}</p>
      <p class="subtitle is-6">{{ entry.description }}</p>
    </div>
    <div class="column has-text-right">
      <p class="is-size-4" :class="{'has-text-danger': entry.amount < 0, 'has-text-success': entry.amount >= 0}">
        <span v-if="entry.amount > 0">+</span>{{ entry.amount }} eb
      </p>
    </div>
  </div>
</div>
</template>

<style scoped>

</style>
// src/stores/userStore.js
import { defineStore } from 'pinia';
import {ref} from "vue";
import ApiConnector from "@/assets/utils/axios/factory.js";
import {useStorage} from "@vueuse/core";

export const useUserStore = defineStore('userStore', () => {
  // State
  const data = ref(null);
  const loading = ref(false);
  const error = ref(null);
  const theme = useStorage('theme', null);

  // Return values for the store
  return {
    data: data,
    loading,
    error,
    theme
  };
});

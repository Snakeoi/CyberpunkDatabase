// src/stores/userStore.js
import { defineStore } from 'pinia';
import {computed, ref} from "vue";
import { useStorage } from "@vueuse/core";
import ApiConnector from "@/assets/utils/axios/factory.js";
import {rolesEnum} from "@/enums.js";

export const useUserStore = defineStore('userStore', () => {
  // State
  const data = ref(null);
  const loading = ref(false);
  const error = ref(null);
  const theme = useStorage('theme', null);

  // Actions
  const fetchUserData = async () => {
    loading.value = true;
    error.value = null;

    try {
      const response = await ApiConnector.get('/user/current');
      data.value = response.data;
    } finally {
      loading.value = false;
    }
  };

  const isAdmin = computed(() => {
    return !!data.value?.permissions?.includes(rolesEnum.admin);
  });

  // Return values for the store
  return {
    data: data,
    loading,
    error,
    theme,
    fetchUserData,
    isAdmin,
  };
});

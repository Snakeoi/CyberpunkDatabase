import { defineStore } from 'pinia';
import {ref} from "vue";

export const adminSettingsViewsStore = defineStore('adminSettingsViewsStore', () => {
  // State
  const characterSearchField = ref('');
  const skillSearchField = ref('');
  const roleSearchField = ref('');

  // Return values for the store
  return {
    userSearchField: characterSearchField,
    skillSearchField: skillSearchField,
    roleSearchField: roleSearchField,
  };
});

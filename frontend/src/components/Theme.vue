<script setup>
import {ref, computed, onMounted} from "vue";
import {useUserStore} from "@/stores/user.js";

const user = useUserStore();
const themeAttributeName = 'data-theme';
const html = ref(document.querySelector('html'));


const setTheme = (valeue) => {
  if (valeue !== null) {
    html.value.setAttribute(themeAttributeName, valeue);
  } else {
    html.value.removeAttribute(themeAttributeName);
  }
  user.theme = valeue;
}

const themes = ref({
  auto: {
    icon: `<span>A</span>`,
    name: 'Auto',
    set: () => {
      setTheme(null);
    }
  },
  light: {
    icon: `<i class="icon-sun-o"></i>`,
    name: 'Jasny',
    set: () => {
      setTheme('light');
    }
  },
  dark: {
    icon: `<i class="icon-moon-o"></i>`,
    name: 'Ciemny',
    set: () => {
      setTheme('dark');
    }
  }
});

const actualTheme = computed(() => {
  const dataThemeValue = user.theme;
  if (dataThemeValue === null) {
    return 'auto';
  } else if (dataThemeValue === 'light') {
    return 'light';
  } else if (dataThemeValue === 'dark') {
    return 'dark';
  }
})
</script>

<template>
  <div class="navbar-item has-dropdown is-hoverable">
    <span class="navbar-link" v-html="themes[actualTheme].icon"></span>
    <div class="navbar-dropdown is-right is-boxed">
      <a v-for="theme in themes"
        @click="theme.set()"
        v-html="theme.icon + theme.name"
        class="navbar-item"
      >
      </a>
    </div>
  </div>
</template>

<style scoped>

</style>
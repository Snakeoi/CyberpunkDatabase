<script setup>
import {useUserStore} from "@/stores/user.js";
import Theme from "@/components/Theme.vue";
import JSLogo from "@/components/JSLogo.vue";

const userStore = useUserStore();
</script>

<template>
<nav class="navbar" role="navigation" aria-label="main navigation">
  <div class="navbar-brand">
    <RouterLink :to="{name: 'home'}" class="navbar-item">
        <JSLogo width="40px"/>
    </RouterLink>

    <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
    </a>
  </div>

  <div class="navbar-menu">
    <div class="navbar-start">
      <RouterLink :to="{name: 'home'}" class="navbar-item">
        Home
      </RouterLink>
    </div>

    <div class="navbar-end">
      <Theme/>
    </div>
  </div>
</nav>
</template>

<style scoped>

</style>
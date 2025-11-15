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
        RedDatabase
      </RouterLink>
    </div>

    <div class="navbar-end">
      <div class="navbar-item">
        <div class="buttons">
          <RouterLink v-if="userStore.isAdmin" :to="{name: 'admin-dashboard'}" class="button is-light is-outlined">
            <span class="icon">
              <i class="icon-cog"></i>
            </span>
          </RouterLink>

          <a class="button is-light is-outlined">
            <span class="icon">
              <i class="icon-user"></i>
            </span>
            <strong>{{ userStore.data?.username }}</strong>
          </a>
          <a class="button is-primary" href="/user/logout">
            <span class="icon">
              <i class="icon-sign-out"></i>
            </span>
            <span>Wyloguj</span>
          </a>
        </div>
      </div>
      <Theme/>
    </div>
  </div>
</nav>
</template>

<style scoped>

</style>
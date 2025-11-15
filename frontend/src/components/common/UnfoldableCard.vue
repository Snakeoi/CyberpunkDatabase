<script setup>
import {ref} from "vue";

const props = defineProps({
  title: {
    type: String,
    required: true
  }
});

const active = ref(false);
</script>

<template>
  <div class="card">
    <header class="card-header is-clickable" @click="active = !active">
      <p class="card-header-title">{{ title }}</p>
      <button class="card-header-icon" aria-label="more options">
        <span class="icon">
          <i v-if="!active" class="icon-angle-down" aria-hidden="true"></i>
          <i v-else class="icon-angle-up" aria-hidden="true"></i>
        </span>
      </button>
    </header>
    <div class="card-content" v-show="active">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped>
.details-tray-header {
  border-top: 1px solid var(--bulma-border);
  border-left: 1px solid var(--bulma-border);
  border-right: 1px solid var(--bulma-border);
}

.details-tray-body {
  border: 1px solid var(--bulma-border);
}
</style>
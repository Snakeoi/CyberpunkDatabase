<script setup>
const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  isActive: {
    type: Boolean,
    default: false,
  },
  icon: {
    type: String,
    default: null,
  },
});
</script>

<template>
<li :class="{'is-active': isActive}">
  <a>
    <span class="icon is-small" v-if="icon"
      ><i :class="icon" aria-hidden="true"></i
    ></span>
    <span>{{ title }}</span>
  </a>
</li>
</template>

<style scoped>

</style>
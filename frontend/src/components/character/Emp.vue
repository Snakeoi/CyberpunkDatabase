<script setup>
const props = defineProps({
  emp: {
    type: Number,
    required: true,
  },
  empBase: {
    type: Number,
    required: true,
  },
  empDebuff: {
    type: Number,
    required: true,
  },
});
</script>

<template>
<div class="level-item has-text-centered">
  <div>
    <p class="heading">EMP (-{{ empDebuff }})</p>
    <p class="title">{{ emp }} / {{ empBase }}</p>
  </div>
</div>
</template>

<style scoped>

</style>
<script setup>

import Tabs from "@/components/Tabs/Tabs.vue";
import Tab from "@/components/Tabs/Tab.vue";

const prps = defineProps({
  tabs: {
    type: Array,
    required: true
  }
});

const model = defineModel()
</script>

<template>
<Tabs>
  <Tab v-for="tab in tabs"
       :key="tab.title"
       :title="tab.title"
       :icon="tab.icon"
       :isActive="model === tab"
       @click.native="model = tab"/>
</Tabs>
</template>

<style scoped>

</style>
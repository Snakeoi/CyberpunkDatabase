<script setup>
import Abilities from '@/components/character/Abilities.vue'
import Ability from '@/components/character/Ability.vue'

const props = defineProps({
  character: Object,
  sheetMode: String
})
</script>

<template>
  <div>
    <div class="box">
      <h2 class="title is-4">Psychika</h2>
      <Abilities>
        <Ability v-model="character.humanity" :editableAt="['play','edit']" :sheetMode="sheetMode" heading="Człowieczeństwo" />
        <Ability v-model="character.emp_base" class="subtitle" :sheetMode="sheetMode" heading="EMP baza" />
        <Ability v-model="character.emp_debuff" class="subtitle" :class="{ 'has-text-danger': character.emp_debuff !== 0 }" heading="EMP kara" />
        <Ability v-model="character.emp" heading="EMP" />
      </Abilities>
    </div>

    <div class="box">
      <h2 class="title is-4">Zdrowie</h2>
      <Abilities>
        <Ability v-model="character.health" :editableAt="['play','edit']" :sheetMode="sheetMode" heading="Zdrowie" />
        <Ability v-model="character.health_base" heading="Max. zdrowie" />
        <Ability v-model="character.serious_wounds" heading="Poważne rany" />
        <Ability v-model="character.survivability" heading="Przeżywalność" />
      </Abilities>
    </div>
  </div>
</template>

<style scoped>
</style>

<script setup>

import {sheetModesEnum} from "@/enums.js";
import {useRoute} from "vue-router";

const route = useRoute();

const model = defineModel({
  type: String,
  default: sheetModesEnum.play
});
</script>

<template>
<div class="tabs is-boxed">
  <ul>
    <li
      v-if="route.params.id"
      @click="model = sheetModesEnum.play"
      :class="{'is-active': model === sheetModesEnum.play}">
      <a>
        <span class="icon is-small"
          ><i class="icon-user" aria-hidden="true"></i
        ></span>Gra
      </a>
    </li>
    <li
        v-if="route.params.id"
        @click="model = sheetModesEnum.edit"
        :class="{'is-active': model === sheetModesEnum.edit}">
      <a>
        <span class="icon is-small"
          ><i class="icon-edit " aria-hidden="true"></i
        ></span>Edycja
      </a>
    </li>
    <li
      v-if="route.params.id"
      @click="model = sheetModesEnum.deleting"
      :class="{'is-active': model === sheetModesEnum.deleting}">
      <a>
        <span class="icon is-small"
          ><i class="icon-trash" aria-hidden="true"></i
        ></span>Usuwanie
      </a>
    </li>
  </ul>
</div>
</template>

<style scoped>

</style>
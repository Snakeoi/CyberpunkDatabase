<script setup>
import {onBeforeMount, onMounted, ref, watch} from "vue";
import {sheetModes} from "@/enums.js";

const props = defineProps({
  heading: {
    type: String,
    required: true,
  },
  sheetMode: {
    type: String,
    default: 'play',
  },
  modelValue: {
    type: Number,
    required: true,
  },
  class: {
    type: String,
  },
  editableAt: {
    type: Array,
    default: ['edit'],
  },
});

const emit = defineEmits([
    'update:modelValue'
]);

const inputValue = ref(props.modelValue);
const pendingValue = ref(0);
let timeoutId = null;

watch(() => props.modelValue, (newValue) => {
  inputValue.value = newValue;
});

function emitValue() {
  if (pendingValue.value !== 0) {
    inputValue.value += pendingValue.value;
    emit('update:modelValue', inputValue.value);
    pendingValue.value = 0;
  }
}

function scheduleEmit() {
  clearTimeout(timeoutId);
  timeoutId = setTimeout(() => {
    emitValue();
  }, 1000);
}

const changeValue = (diff) => {
  pendingValue.value += diff;
  scheduleEmit();
};
</script>

<template>
<div class="level-item has-text-centered">
  <div>
    <p class="heading">{{ heading }}</p>
    <p class="title is-4" :class="props.class">{{ inputValue + pendingValue }}</p>
    <span v-if="props.editableAt.includes(sheetMode)" @mouseleave="emitValue" class="has-text-primary">
      <i
        @click="changeValue(-1)"
        class="icon-minus-square is-clickable pr-4">
      </i>
      <i
        @click="changeValue(1)"
        class="icon-plus-square is-clickable">
      </i>
    </span>
  </div>
</div>
</template>
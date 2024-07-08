<script setup>
import { defineProps, computed } from 'vue';

const props = defineProps(['date']);

const [day, month, year] = props.date.split('.').map(Number);
const date = new Date(year, month - 1, day);

const text = computed(() => {
  const text = date.toLocaleDateString('en-EN', { weekday: 'short' })
  return `${text} ${date.getDate()}`;
})

const isToday = computed(() => {
  if (new Date().getDate() === date.getDate()) {
    return true
  } else {
    return false
  }
})
</script>

<template>
  <span class="planner-date"
    :class="{'current': isToday}"
  >{{ text }}</span>
</template>

<style lang="scss">
  .planner-date {
    @include bold-18;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: size(32px);
    background-color: $white;

    &.current {
      color: $blue-attention;
    }
  }
</style>
<script setup>
import { defineProps, computed } from 'vue';

const props = defineProps(['day']);
</script>

<template>
  <div class="planner-date"
    :class="{'current': day.isToday}"
  > 
    <span class="planner-date__weekday">{{ day.weekday }}</span>
    <div class="planner-date__day">
        <span>{{ day.date }}</span>
    </div>
  </div>
</template>

<style lang="scss">
  .planner-date {
    width: 100%;
    background-color: $white;
    padding-bottom: size(12px);
    position: relative;

    &::before {
      content: '';
      display: block;
      width: 1px;
      height: size(45px);
      position: absolute;
      left: 0;
      bottom: 0;
      border-left: 1px solid $dark-lines;
    }

    &.current {
      & .planner-date__weekday {
        color: $blue-attention;
      }

      & .planner-date__day {
        color: $white;
        position: relative;

        & span {
          position: relative;
          z-index: 2;
        }

        &::before {
          content: '';
          display: block;
          width: size(40px);
          height: size(40px);
          background-color: $blue-attention;
          border-radius: 50%;
          position: absolute;
          left: 50%;
          top: calc(50% + size(2px));
          transform: translate(-50%, -50%)
        }
      }
    }

    &__weekday {
      @include small-bold;
      display: block;
      margin-bottom: size(3px);
      text-align: center;
    }

    &__day {
      @include header;
      display: block;
      text-align: center;
    }
  }
</style>
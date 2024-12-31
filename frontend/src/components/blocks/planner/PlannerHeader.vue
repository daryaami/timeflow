<script setup>
import { computed } from 'vue';
import { useCurrentDateStore } from '@/store/currentDate';

const emit = defineEmits(['prevWeek', 'nextWeek']);

const currentDate = useCurrentDateStore()

const props = defineProps(['isSidebarOpened', 'isLoading']);

const isSidebarOpened = defineModel();

const currentMonth = computed(() => {
  if (currentDate.date) {
    const now = currentDate.date;
    return `${now.toLocaleString('default', { month: 'long' })} ${now.getFullYear()}`;
  } else {
    return ''
  }
})

const nextWeekHandler = async () => {
  if (props.isLoading) return
  currentDate.toNextWeek()
}

const prevWeekHandler = async () => {
  if (props.isLoading) return
  currentDate.toPrevWeek()
}
</script>

<template>
  <header class="planner-header">
    <span class="planner-header__date">{{ currentMonth }}</span>
    <div class="planner-header__buttons">
      <button class="planner-header__date-button planner-header__date-button--prev icon-button"
        @click="prevWeekHandler"
      ></button>
      <button class="planner-header__date-button planner-header__date-button--next icon-button"
        @click="nextWeekHandler"
      ></button>
    </div>


    <label class="sidebar-hide icon-button"
      :class="{rotated: !isSidebarOpened}"
    >
      <input type="checkbox" class="visually-hidden"
        v-model="isSidebarOpened"
      >
    </label>
  </header>
</template>

<style lang="scss">
.planner-header {
  padding-left: size(79px);
  padding-right: size(24px);
  height: size(80px);
  display: flex;
  align-items: center;

  &__date {
    @include bold-title-24;
    display: block;
    width: size(200px);
  }

  &__buttons {
    display: flex;
    margin-left: size(87px);
    gap: size(14px);
  }

  &__date-button {
    display: block;
    width: size(36px);
    height: size(36px);
    background-size: size(24px) size(24px);
    background-position: center;

    &--prev {
      @include chevron-left;
    }

    &--next {
      @include chevron-right;
    }
  }

  .sidebar-hide {
    margin-left: auto;
    @include sidebar-hide;
    background-position: center;
    background-size: size(24px) size(24px);
    width: size(48px);
    height: size(48px);
    cursor: pointer;
    margin-left: auto;

    &.rotated {
      transform: rotate(180deg);
    }
  }
}
</style>
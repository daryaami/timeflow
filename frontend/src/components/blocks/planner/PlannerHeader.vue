<script setup>
const emit = defineEmits(['prevWeek', 'nextWeek']);

const props = defineProps(['isSidebarOpened', 'currentMonth']);

const isSidebarOpened = defineModel();
</script>

<template>
  <header class="planner-header">
    <span class="planner-header__date">{{ currentMonth }}</span>
    <div class="planner-header__buttons">
      <button class="planner-header__date-button planner-header__date-button--prev icon-button"
        @click="emit('prevWeek')"
      ></button>
      <button class="planner-header__date-button planner-header__date-button--next icon-button"
        @click="emit('nextWeek')"
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
    @include reset-button;
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
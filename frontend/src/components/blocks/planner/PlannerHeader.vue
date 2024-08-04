<script setup>
const props = defineProps('isSidebarOpened');

const isSidebarOpened = defineModel();


</script>

<template>
  <header class="planner-header">
    <div class="planner-header__date">
      <span>February 2024</span>
      <div class="planner-header__date-buttons">
        <button class="planner-header__date-button planner-header__date-button--prev"></button>
        <button class="planner-header__date-button planner-header__date-button--next"></button>
      </div>


      <label class="sidebar-hide icon-button"
        :class="{rotated: !isSidebarOpened}"
      >
        <input type="checkbox" class="visually-hidden"
          v-model="isSidebarOpened"
        >
      </label>
    </div>
  </header>
</template>

<style lang="scss">
.planner-header {
  padding: size(21px) size(27px) size(21px) size(46px);

  &__date {
    @include bold-title-24;
    font-weight: 400;
    display: flex;
    gap: size(49px);
    align-items: center;
  }

  &__date-buttons {
    display: flex;
    gap: size(27px);
  }

  &__date-button {
    @include reset-button;
    display: block;
    width: size(25px);
    height: size(25px);
    background-size: 100%;

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

    &.rotated {
      transform: rotate(180deg);
    }
  }
}
</style>
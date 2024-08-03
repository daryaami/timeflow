<template>
  <header class="planner-header">
    <div class="planner-header__date">
      <span>February 2024</span>
      <div class="planner-header__date-buttons">
        <button class="planner-header__date-button planner-header__date-button--prev"></button>
        <button class="planner-header__date-button planner-header__date-button--next"></button>
      </div>

      <button 
        class="sidebar-hide"
        :class="{rotated: isSidebarHidden}"
        @click="$emit('update:isSidebarHidden', !isSidebarHidden)"
      ></button>
    </div>
  </header>
</template>

<script>
export default {
  props: {
    isSidebarHidden: Boolean,
  },
  emits: {
    'update:isSidebarHidden': Boolean,
  },
}
</script>

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
    @include reset-button;
    @include sidebar-hide;
    background-size: size(24px) size(24px);
    width: size(32px);
    height: size(32px);

    &.rotated {
      transform: rotate(180deg);
    }
  }
}
</style>
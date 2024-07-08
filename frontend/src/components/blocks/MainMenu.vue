<script setup>
const menuItems = [
  {
    title: 'Calendar',
    class: 'main-menu__link--calendar',
    isCurrent: true,
  },
  {
    title: 'Tasks',
    class: 'main-menu__link--tasks',
  },
  {
    title: 'Habits',
    class: 'main-menu__link--habits',
  },
  {
    title: 'Settings',
    class: 'main-menu__link--settings',
  },
]
</script>

<template>
  <nav>
    <ul class="main-menu__list">
      <li 
        v-for="item in menuItems"
        :key="item.title"
      >
        <a href="#" class="main-menu__link"
          :class="[{'current': item.isCurrent}, item.class]"
        >{{ item.title }}</a>
      </li>
    </ul>
    
  </nav>
</template>



<style lang="scss">
.main-menu {
  &__list {
    padding: 0;
    margin: 0;
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: size(19px);
  }

  &__link {
    display: block;
    padding: size(14px);
    padding-left: size(56px);
    background-repeat: no-repeat;
    background-position: size(23px) center;
    border-radius: size(15px);
    background-size: size(20px) size(20px);

    &--calendar {
      @include calendar-icon;
    }

    &--tasks {
      @include tasks-icon;
    }

    &--habits {
      @include habits-icon;
    }

    &--settings {
      @include settings-icon;
    }

    &.current {
      background-color: #474B59;
    }

    &:not(.current):hover {
      background-color: #3E414E;
    }
  }

}
</style>
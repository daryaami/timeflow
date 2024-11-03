<script setup>
const menuItems = [
  {
    title: 'Calendar',
    icon: '#calendar-icon',
    isCurrent: true,
  },
  {
    title: 'Tasks',
    icon: '#tasks-icon',
  },
  {
    title: 'Habits',
    icon: '#habits-icon',
  },
  {
    title: 'Statistics',
    icon: '#stats-icon',
  },
  {
    title: 'Settings',
    icon: '#settings-icon',
  },
]
</script>

<template>
  <nav class="main-menu">
    <ul class="main-menu__list">
      <li 
        v-for="item in menuItems"
        :key="item.title"
      >
        <a href="#" class="main-menu__link"
          :class="[{'current': item.isCurrent}]"
        >
          <svg width="20" height="20">
            <use :xlink:href="item.icon" />
          </svg>
          <span>{{ item.title }}</span>
        </a>
      </li>
    </ul>
    
  </nav>
</template>



<style lang="scss">
.main-menu {
  padding: 0 size(26px);

  &__list {
    padding: 0;
    margin: 0;
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: size(8px);
  }

  &__link {
    display: flex;
    align-items: center;
    gap: size(13px);
    padding: size(19px) size(23px);
    background-repeat: no-repeat;
    background-position: size(23px) center;
    border-radius: size(15px);
    background-size: size(20px) size(20px);
    @include bold-title-24;


    &.current {
      background-color: $dark-lines;
    }

    &:not(.current):hover {
      background-color: $dark-lines;
    }
  }

}
</style>
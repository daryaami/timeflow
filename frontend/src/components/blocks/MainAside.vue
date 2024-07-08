<script setup>
import MainMenuVue from "./MainMenu.vue";
</script>

<template>
  <div class="main-aside">
    <div class="main-aside__title-wrapper">
      <h1 class="main-aside__title">Timeflow</h1>
      <div class="main-aside__button">
      </div>
    </div>
    <MainMenuVue />
  </div>
</template>


<style lang="scss">
.main-aside {
  width: size(404px);
  height: 100%;
  background-color: #363945;
  display: block;
  padding: 20px 26px;
  color: #f5f5f5;

  &__title-wrapper {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 40px;
  }

  &__title {
    margin: 0;
  }

  &__button {
    width: size(25px);
    height: size(25px);

    & svg {
      display: block;
      widows: 100%;
      height: 100%;
    }
  }
}
</style>
<script setup>
// import "@/assets/scss/global.scss";
import { RouterLink, RouterView, useRoute } from 'vue-router'
const route = useRoute()
</script>

<template>
  <div class="container">
    <RouterView v-if="route.meta.loginPage" />

  <header v-if="false">

        <div class="wrapper">
          <HelloWorld msg="You did it!" />

          <nav>
            <RouterLink to="/habits">Habits</RouterLink>
            <RouterLink to="/tasks">Tasks</RouterLink>
          </nav>
        </div>

      </header>
  </div>
</template>

<style lang="scss">
  .container {
    width: 100%;
    height: 100%;
  }
</style>


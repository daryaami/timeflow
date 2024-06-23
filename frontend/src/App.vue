<script setup>
import loginLayout from './components/layouts/login-layout.vue';
import { useRoute } from 'vue-router';
const route = useRoute()
</script>

<template>
  <div class="container">
    <loginLayout v-if="route.meta.loginPage"/>
  
  </div>
</template>

<style lang="scss">
  .container {
    width: 100%;
    height: 100%;
  }
</style>


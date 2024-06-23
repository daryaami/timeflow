<script setup>
import { useRoute } from 'vue-router';
import LoginLayout from './components/layouts/LoginLayout.vue';
import DefaultLayout from './components/layouts/DefaultLayout.vue';

const route = useRoute();
</script>

<template>
  <div class="container">
    <LoginLayout v-if="route.meta.layout == 'login'" />
    <DefaultLayout v-if="route.meta.layout == 'default'"/>
  </div>
</template>

<style lang="scss">
.container {
  width: 100%;
  height: 100%;
}
</style>

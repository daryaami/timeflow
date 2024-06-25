<script setup>
import MainAsideVue from "../blocks/MainAside.vue";
import PageHeaderVue from "../blocks/PageHeader.vue";
import { useRoute } from 'vue-router';
const route = useRoute()
</script>

<template>
  <div class="page-wrapper">
    <MainAsideVue />
    <div class="page-wrapper__main">
      <PageHeaderVue 
        :title="route.meta.title"
      />
      <RouterView  />
    </div>
  </div>
</template>

<style lang="scss">
.page-wrapper {
  display: flex;
  width: 100%;
  height: 100%;
  align-items: flex-start;

   &__main {
    flex-basis: 100%;
    flex-shrink: 1;
    display: flex;
    flex-direction: column;
    height: 100%;
  }
}
</style>

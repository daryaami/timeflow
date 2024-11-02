<script setup>
import MainAsideVue from "../components/blocks/MainAside.vue";
import PageHeaderVue from "../components/blocks/PageHeader.vue";
import { useRoute } from 'vue-router';

import { userData } from "../components/js/data/userData";
import { getUserData } from "../components/js/getUserData";
import { onMounted } from "vue";

const route = useRoute();

onMounted(async () => {
  userData.value = await getUserData();
})
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
    height: 100%;
    display: grid;
    grid-template-rows: auto 1fr;
  }
}
</style>

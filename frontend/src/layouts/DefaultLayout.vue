<script setup>
import MainAsideVue from "../components/blocks/main-aside/MainAside.vue";
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
    <PageHeaderVue 
      :title="route.meta.title"
    />
    <div class="page-wrapper__main">
      <MainAsideVue />
      <RouterView  />
    </div>
  </div>
</template>

<style lang="scss">
.page-wrapper {
  width: 100%;
  height: 100%;
  display: grid;
  grid-template-rows: min-content 1fr;

  &__main {
    display: flex;
    width: 100%;
    flex-grow: 1;
    overflow: auto;
  }
}
</style>

<script setup>
import NewTaskBlockVue from './new-task/NewTaskBlock.vue';
import SearchBlock from './SearchBlock.vue'

import logoIcon from '@/assets/img/logo.svg';

const props = defineProps({
  title: String,
});

</script>


<template>
  <div class="page-header">
    <div class="page-header__title-wrapper">
      <img :src="logoIcon" alt="TimeFlow" width="40" height="40">

      <h1 class="page-header__title">TimeFlow</h1>
    </div>
    <new-task-block-vue/>
    <search-block />
  </div>
</template>


<style lang="scss">
.page-header {
  display: flex;
  align-items: center;
  gap: 41px;
  width: 100%;
  padding: size(20px) size(17px) size(20px) size(46px);
  border-bottom: 1px solid $light-lines;

  &__title-wrapper {
    margin-right: auto;
    display: flex;
    align-items: center;
    gap: 15px;

    & img {
      display: block;
      width: size(40px);
      height: size(40px);
    }
  }

  &__title {
    font-weight: 400;
    font-size: size(34px);
    line-height: 100%;
    letter-spacing: -0.04em;
    color: $basic-dark;
    margin: 0;
  }
}
</style>
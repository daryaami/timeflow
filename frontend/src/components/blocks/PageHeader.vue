<script setup>
import NewTaskBlockVue from './new-task/NewTaskBlock.vue';
import SearchBlock from './SearchBlock.vue'
import { userData } from '../js/data/userData';

const props = defineProps({
  title: String,
});

</script>


<template>
  <div class="page-header">
    <!-- <h1>{{ title }}</h1> -->
    <new-task-block-vue v-if="userData" />
    <search-block />
  </div>
</template>


<style lang="scss">
.page-header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 41px;
  width: 100%;
  padding: 20px 17px;
  border-bottom: 1px solid $light-lines;
}
</style>
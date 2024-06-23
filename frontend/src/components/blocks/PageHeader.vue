<script setup>
import SearchBlock from './SearchBlock.vue'

const props = defineProps({
  title: String,
});

</script>


<template>
  <div class="page-header">
    <h1>{{ title }}</h1>
    <button class="page-header__add-task">+ New Task</button>
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

  &__add-task {
    @include reset-button;
    @include hover {
      color: $light-grey;
    }
  }  
}
</style>
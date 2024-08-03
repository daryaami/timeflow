<script setup>
const props = defineProps(['task'])
</script>

<template>
  <div class="task">
    <span class="task__color"
    :style='{
      backgroundColor: task.color,
    }'
    ></span>
    <label 
      class="task__checkbox-label"
      :for="title"
    >
      <input class="visually-hidden" :id="title" type="checkbox">
    </label>
    <span>{{ task.name }}</span>
  </div>
</template>

<style lang="scss">
.task {
  @include light-20;
  display: flex;
  align-items: center;
  gap: size(10px);
  position: relative;
  overflow: hidden;
  height: size(68px);
  padding: size(19px) size(17px) size(19px) size(25px);
  border-radius: size(15px);
  background-color: white;

  &__color {
    display: block;
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    width: size(10px);
    background-color: #F0F0F0;
  }
  

  &__checkbox-label {
    display: block;
    width: size(28px);
    height: size(28px);
    @include empty-checkbox;
    background-size: 100%;
    cursor: pointer;
    transition: .1s;
    flex-shrink: 0;

    &:has(:checked) {
      @include checked-checkbox;
    }
  }
}
</style>
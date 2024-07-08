<script setup>
import googleIcon from '@/assets/img/google-icon.png'

const props = defineProps({
  href: String,
  text: String,
});
</script>

<template>
  <a class="google-button" :href="href">
    <img class="google-button__icon" width="50" height="50"
      :src="googleIcon" 
      alt="Google logo">
    <span>{{ text }}</span>
  </a>
</template>

<style lang="scss">
  .google-button {
    @include bold-20;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: size(50px);
    height: size(76px);
    width: size(391px);
    background-color: #ABFFF0;
    color: $darkest;
    gap: size(8px);

    &__icon {
      display: block;
      width: size(50px);
      height: size(50px);
    }
  }
</style>
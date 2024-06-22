<script>
import googleIcon from '@/assets/img/google-icon.png'

export default {
  props: ['href', 'text'],
  data() {
    return {
      googleIcon
    }
  },
}
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
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: size(50px);
    height: size(76px);
    width: size(391px);
    background-color: #ABFFF0;
    font-weight: 500;
    font-size: size(20px);
    color: $darkest;
    gap: size(8px);

    &__icon {
      display: block;
      width: size(50px);
      height: size(50px);
    }
  }
</style>
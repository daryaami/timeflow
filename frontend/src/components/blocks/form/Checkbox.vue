<script setup>
const props = defineProps({
  label: {
    type: String,
  },
  buttons: {
    type: Boolean,
    default: false,
  },
});

const value = defineModel();
</script>

<template>
  <label class="checkbox">
    <input type="checkbox" class="visually-hidden" v-model="value">
    <span class="checkbox__label">{{ label }}</span>
  </label>
</template>

<style lang="scss">
  .checkbox {
    display: flex;
    align-items: center;
    height: size(28px);
    padding-left: size(30px);
    background-image: url("data:image/svg+xml,%3Csvg width='28' height='28' viewBox='0 0 28 28' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M22.75 3.5H5.25C4.78587 3.5 4.34075 3.68437 4.01256 4.01256C3.68437 4.34075 3.5 4.78587 3.5 5.25V22.75C3.5 23.2141 3.68437 23.6592 4.01256 23.9874C4.34075 24.3156 4.78587 24.5 5.25 24.5H22.75C23.2141 24.5 23.6592 24.3156 23.9874 23.9874C24.3156 23.6592 24.5 23.2141 24.5 22.75V5.25C24.5 4.78587 24.3156 4.34075 23.9874 4.01256C23.6592 3.68437 23.2141 3.5 22.75 3.5ZM5.25 22.75V5.25H22.75V22.75H5.25Z' fill='%235D6170'/%3E%3C/svg%3E%0A");
    background-repeat: no-repeat;
    background-position: left center;
    background-size: size(28px) size(28px);
    cursor: pointer;

    &:has(:checked) {
      background-image: url("data:image/svg+xml,%3Csvg width='28' height='28' viewBox='0 0 28 28' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cg clip-path='url(%23clip0_359_261)'%3E%3Cpath d='M22.75 3.5H5.25C4.78587 3.5 4.34075 3.68437 4.01256 4.01256C3.68437 4.34075 3.5 4.78587 3.5 5.25V22.75C3.5 23.2141 3.68437 23.6592 4.01256 23.9874C4.34075 24.3156 4.78587 24.5 5.25 24.5H22.75C23.2141 24.5 23.6592 24.3156 23.9874 23.9874C24.3156 23.6592 24.5 23.2141 24.5 22.75V5.25C24.5 4.78587 24.3156 4.34075 23.9874 4.01256C23.6592 3.68437 23.2141 3.5 22.75 3.5ZM12.25 18.8125L7.875 14.4749L9.26695 13.125L12.25 16.0524L18.7326 9.625L20.1254 11.005L12.25 18.8125Z' fill='%233B61E8'/%3E%3C/g%3E%3Cdefs%3E%3CclipPath id='clip0_359_261'%3E%3Crect width='28' height='28' fill='white'/%3E%3C/clipPath%3E%3C/defs%3E%3C/svg%3E%0A");
    }


    &__label {
      @include light-16;
      white-space: nowrap;
    }
  }
</style>

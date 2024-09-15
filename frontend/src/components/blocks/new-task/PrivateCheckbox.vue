<script setup>
  const isPrivate = defineModel()
</script>

<template>
  <label class="private-checkbox">
    <input class="visually-hidden" type="checkbox" name="visibility" v-model="isPrivate" >
  </label>
</template>

<style lang="scss">
.private-checkbox {
  display: block;
  width: size(30px);
  height: size(30px);
  background-position: center;
  transition: .2s;
  background-size: 100%;
  background-image: url("data:image/svg+xml,%3Csvg width='30' height='30' viewBox='0 0 30 30' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M1 14.5C9.4 3.16667 20.6 3.16667 29 14.5C20.6 25.8333 9.4 25.8333 1 14.5Z' stroke='%233B61E8' stroke-width='2' stroke-linejoin='round'/%3E%3Cpath d='M19 14C19 15.0609 18.5786 16.0783 17.8284 16.8284C17.0783 17.5786 16.0609 18 15 18C13.9391 18 12.9217 17.5786 12.1716 16.8284C11.4214 16.0783 11 15.0609 11 14C11 12.9391 11.4214 11.9217 12.1716 11.1716C12.9217 10.4214 13.9391 10 15 10C16.0609 10 17.0783 10.4214 17.8284 11.1716C18.5786 11.9217 19 12.9391 19 14Z' stroke='%233B61E8' stroke-width='2' stroke-linejoin='round'/%3E%3C/svg%3E%0A");
  cursor: pointer;

  &.private {
    background-image: url("data:image/svg+xml,%3Csvg width='30' height='30' viewBox='0 0 30 30' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M1 9C2.33561 10.7624 3.90903 12.2944 5.66667 13.5438M5.66667 13.5438C7.55855 14.888 9.67135 15.8218 11.8889 16.2938C13.9441 16.7239 16.0559 16.7239 18.1111 16.2938C20.3287 15.8218 22.4415 14.888 24.3333 13.5438M5.66667 13.5438L3.33333 16.6154M29 9C27.6644 10.7624 26.091 12.2944 24.3333 13.5438M24.3333 13.5438L26.6667 16.6154M11.8889 16.2922L11.1111 20M18.1111 16.2922L18.8889 20' stroke='%233B61E8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E%0A");
  }
}
</style>
<template>
  <div class="search">
    <button class="search__button">
    
    </button>
  </div>
</template>

<script>
export default {
  
}
</script>

<style lang="scss">
.search {
  &__button {
    @include reset-button;
    @include search-icon;
    width: size(24px);
    height: size(24px);
    display: block;
    background-size: 100%;
  }
}
</style>
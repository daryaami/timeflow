<template>
 <div class="loading-container">
    <div class="loading-progress"></div>
  </div>
</template>

<style lang="scss">
.loading-container {
  position: relative;
  height: size(70px);
  width: size(70px);
}

.loading-progress {
  position: absolute;
  height: 100%;
  width: 100%;
  border-radius: 50%;
  border: 5px solid #67DEC9;
  border-radius: 50%;
  
  &::before {
    content: "";
    position: absolute;
    height: 100%;
    width: 100%;
    border-radius: 50%;
    border: 5px solid transparent;
    border-top-color: #482255;
    top: -5px;
    left: -5px;
    animation: spin 1s linear infinite;
  }
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  
  100% {
    transform: rotate(360deg);
  }
}
</style>
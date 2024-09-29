<script setup>
</script>

<template>
  <div class="loader">
    <svg width="200" height="200" viewBox="0 0 200 200">
      <circle cx="100" cy="100" r="90"></circle>
    </svg>
    <svg width="200" height="200" viewBox="0 0 200 200">
      <circle cx="100" cy="100" r="90"></circle>
    </svg>
    <svg width="200" height="200" viewBox="0 0 200 200">
      <circle cx="100" cy="100" r="90"></circle>
    </svg>
  </div>
</template>

<style lang="scss">
.loader {
  position: relative;
  height: 100%;
  aspect-ratio: 1 / 1;
}

.loader svg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.loader svg circle {
  fill: none;
  stroke: #fff;
  stroke-width: 20px;
  stroke-linecap: round;
  animation: animate 2s linear infinite;
}

.loader svg:nth-child(1) circle {
  stroke: #43acff;
}

.loader svg:nth-child(2) circle {
  stroke: #43acff;
}

.loader svg:nth-child(3) circle {
  stroke: $white;
}

@keyframes animate {
  0% {
    stroke-dasharray: 566;
    stroke-dashoffset: 566;
  }
  50% {
    stroke-dasharray: 566;
    stroke-dashoffset: 0;
  }
  100% {
    stroke-dasharray: 566;
    stroke-dashoffset: -566;
  }
}
</style>
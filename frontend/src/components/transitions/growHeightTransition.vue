<script setup>

const onBeforeEnter = el => {
  el.style.transition = '.2s'
  el.style.height = 0;
  el.style.overflow = 'hidden';
}

const onEnter = el => {
  el.classList.add('active');
  el.style.height = `${el.scrollHeight}px`
  el.style.overflow = 'visible'
}


const onBeforeLeave = el => {
  el.style.height = '0px'
  el.classList.remove('active');
  el.style.overflow = 'hidden'
}

const onLeave = el => {

}

</script>

<template>
  <Transition
    name="grow-height-transition"
    @before-enter="onBeforeEnter"
    @enter="onEnter"
    @before-leave="onBeforeLeave"
    @leave="onLeave"
  >
    <slot></slot>
  </Transition>
</template>
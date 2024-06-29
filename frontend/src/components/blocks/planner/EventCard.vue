<script setup>
import { computed } from 'vue';
import { getDecimalHours, getStringTime } from '@/components/js/time-utils';

const props = defineProps(['event']);

const position = computed((() => getDecimalHours(props.event.start.dateTime) * 100 / 24));

const height = computed(() => {
  const duration = getDecimalHours(props.event.end.dateTime) - getDecimalHours(props.event.start.dateTime);
  return duration * 100 / 24
})

const time = computed(() => `${getStringTime(props.event.start.dateTime)} - ${getStringTime(props.event.end.dateTime)}`);
</script>

<template>
  <div class="event-card"
    :style='{
      top: `${position}%`,
      height: `${height}%`,
    }'
  >
    <span class="event-card__name">{{ event.summary }}</span>
    <span class="event-card__time">{{ time }}</span>
  </div>
  
</template>

<style lang="scss">
.event-card {
  padding: size(8px);
  background-color: #E68D8D;
  color: $white;
  border-radius: size(10px);
  height: size(90px);
  width: calc(100% - size(15px));
  position: absolute;
  left: 0;

  &__name {
    font-weight: 400;
    font-size: size(14px);
    line-height: 100%;
    margin-bottom: size(4px);
    display: block;
  }

  &__time {
    font-weight: 300;
    font-size: size(14px);
    line-height: 100%;
    color: $white;
  }
}
</style>
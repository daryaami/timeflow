<script setup>
import { computed, ref } from 'vue';
import { getDecimalHours, getStringTime } from '@/components/js/time-utils';

const props = defineProps(['event']);

const duration = ref(getDecimalHours(props.event.end.dateTime) - getDecimalHours(props.event.start.dateTime))
const startTime = ref(getStringTime(props.event.start.dateTime));

const position = computed((() => getDecimalHours(props.event.start.dateTime) * 100 / 24));

const height = computed(() => {
  return duration.value * 100 / 24
})

const time = computed(() => `${startTime.value} - ${getStringTime(props.event.end.dateTime)}`);
const isPast = computed(() => {
  if (new Date(props.event.end.dateTime) < new Date()) {
    return true
  } else {
    return false
  }
})
</script>

<template>
  <div class="event-card"
    :style='{
      top: `${position}%`,
      height: `calc(${height}% - 2px)`,
      backgroundColor: `${event.background_color}`,
      color: `${event.foreground_color}`,
    }'
    
    :class="{
      'no-padding': duration <= .25,
      'no-right-padding': duration <= .5,
      'past': isPast,
    }"
  >
    <div v-if="duration <= 0.5"
      class="event-card__short-wrapper"
    >
      <span class="event-card__name">{{ event.summary }},&nbsp;</span>
      <span class="event-card__time">{{ startTime }}</span>
    </div>
    <div class="event-card__name-wrapper">
      <span class="event-card__name"
        v-if="duration > 0.5"
        :class="{
          'one-string': duration <= 1,
        }"
      >{{ event.summary }}</span>
    </div>
      
    <span class="event-card__time"
      v-if="duration > 0.5"
    >{{ time }}</span>
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
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: start;

  &.no-padding {
    padding-top: 0;
    padding-bottom: 0;
  }

  &.no-right-padding {
    padding-right: 0;
  }

  &.past {
    opacity: .5;
  }

  &__short-wrapper {
    display: flex;

    & .event-card__name {
      flex-shrink: 0;
    }
  }

  &__name-wrapper {
    overflow: hidden
  }

  &__name {
    @include small-bold;
    margin-bottom: size(4px);
    display: block;
    color: inherit;
  }

  &__time {
    @include small-light;
    color: inherit;
    display: block;
  }
}

.one-string {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  line-clamp: 1;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
<script setup>
import { defineProps, defineEmits, computed } from 'vue';
import { getStringTime } from '@/components/js/time-utils';

import closeIcon from '@/components/icons/close-icon.vue';

const props = defineProps(['event']);
const emit = defineEmits(['close']);

const duration = computed(() => {
  const start = new Date(props.event.start.dateTime);
  const end = new Date(props.event.end.dateTime);
  const durationMs = end - start;
  const hours = Math.floor(durationMs / (1000 * 60 * 60));
  const minutes = Math.floor((durationMs % (1000 * 60 * 60)) / (1000 * 60));

  return `${hours} hr${hours > 1? 's': ''}${minutes > 0? ` ${minutes} min`: ''}`
})


const dates = computed(() => {
  const startDate = new Date(props.event.start.dateTime);
  const endDate = new Date(props.event.end.dateTime);

  return `${startDate.getDate()}/${startDate.getMonth()} ${getStringTime(startDate)} - ${getStringTime(endDate)}`
})

</script>

<template>
  <div class="event-info-sidebar">
    <div class="event-info-sidebar__buttons-wrapper">
      <button class="event-info-sidebar__button icon-button"
        @click="emit('close')"
      >
        <close-icon />
      </button>
    </div>

    <span class="event-info-sidebar__event-title">{{ event.summary }}</span>

    <ul class="event-characteristics">
      <li>
        <span class="event-characteristics__name">Duration</span>
        <span class="event-characteristics__value">{{ duration }}</span>
      </li>
      <li>
        <span class="event-characteristics__name">Dates</span>
        <span class="event-characteristics__value">{{ dates }}</span>
      </li>
      <li v-if="event.calendar">
        <span class="event-characteristics__name">Calendar</span>
        <span class="event-characteristics__value">{{ event.calendar }}</span>
      </li>
    </ul>
  </div>
</template>

<style lang="scss">
.event-info-sidebar {
  background-color: $white;
  padding: size(28px) size(28px) size(28px) size(40px);
  
  &__buttons-wrapper {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 8px;
    margin-bottom: 56px;
  }


  &__button {
    width: size(24px);
    height: size(24px);

    & svg {
      width: 100%;
      height: 100%;
    }
  }

  &__event-title {
    display: block;
    @include bold-20;
    margin-bottom: 56px;
  }

  .event-characteristics {
    @include reset-list;
    display: flex;
    flex-direction: column;
    gap: 16px;

    &__name {
      @include small-bold;
      display: block;
      margin-bottom: 8px;
    }

    &__value {
      display: block;
      @include small-light;
    }
  }
}
</style>
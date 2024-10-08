<script setup>
import { ref, onMounted, nextTick, computed, watch } from 'vue';
import { userData } from '@/components/js/data/userData';
import { isSameDay } from '@/components/js/time-utils';
import { getCurrentWeekMonday } from '@/components/js/time-utils';

import PlannerGrid from '@/components/blocks/planner/PlannerGrid.vue';

import PlannerHeaderVue from '../components/blocks/planner/PlannerHeader.vue';
import LoaderVue from '../components/blocks/loaders/Loader.vue';

import { getEvents, updatedEvents } from '@/components/js/data/events';

import PlannerDateVue from '../components/blocks/planner/PlannerDate.vue';
import RightSidebarVue from '@/components/blocks/planner/RightSidebar.vue';

const isSidebarOpened = ref(true);
const days = ref([])

// Get events

const isLoading = ref(true);

const createOverlappingEvents = (events) => {
  const sortedEvents = events.sort((a, b) => new Date(a.start.dateTime) - new Date(b.start.dateTime))

  for(let i = 1; i < sortedEvents.length; i++) {
    const currentEvent = sortedEvents[i];
    const currentEventStartDate = new Date(currentEvent.start.dateTime);

    for(let j = i - 1; j >= 0; j--) {
      const compEvent = sortedEvents[j]
      if (currentEventStartDate > new Date(compEvent.start.dateTime) && currentEventStartDate < new Date(compEvent.end.dateTime)) {
        compEvent.overlapLevel? 
          currentEvent.overlapLevel = compEvent.overlapLevel + 1:
          currentEvent.overlapLevel = 1;
        
        break;
      }
    }
  }
  
  return sortedEvents
}

const createDays = (date, events) => {
  const monday = getCurrentWeekMonday(date)

  days.value = [];
  for (let i = 0; i < 7; i++) {
    const day = new Date(monday);
    day.setDate(monday.getDate() + i); 

    const filteredEvents = events.filter(event => 
      isSameDay(day, new Date(event.start.dateTime)) || 
      isSameDay(day, new Date(event.end.dateTime))
    )

    days.value.push({
      weekday: day.toLocaleDateString('en-EN', { weekday: 'short' }),
      date: day.getDate(),
      isToday: isSameDay(day, new Date()),
      day: day,
      events: createOverlappingEvents(filteredEvents),
    });
  }
}

const fetchData = async (date = new Date()) => {
  try {
    const events = await getEvents(date);
    createDays(date, events)
  } catch (error) {
    console.error('ошибка', error);
  } finally {
    isLoading.value = false;
    await nextTick();
  }
}

const nextWeekHandler = async () => {
  if (isLoading.value) return
  isLoading.value = true;
  
  const date = days.value[0].day;
  const nextMonday = new Date(date.setDate(date.getDate() + 7));

  fetchData(nextMonday);
}

const prevWeekHandler = async () => {
  if (isLoading.value) return
  isLoading.value = true;
  const date = days.value[0].day;
  const prevMonday = new Date(date.setDate(date.getDate() - 7));
  fetchData(prevMonday)
}

// Current Month

const currentMonth = computed(() => {
  if (days.value.length) {
    const now = days.value[0].day;
    return `${now.toLocaleString('default', { month: 'long' })} ${now.getFullYear()}`;
  } else {
    return ''
  }
})

onMounted(() => {
  fetchData();
})

watch(updatedEvents, (newEvents) => {
  newEvents.forEach(event => {
    const dayToUpdate = days.value.find(day => 
      isSameDay(day.day, new Date(event.start.dateTime)) || 
      isSameDay(day.day, new Date(event.end.dateTime))
    )
    if (dayToUpdate) {
      dayToUpdate.events.push(event);
    }
  })
})
</script>

<template>
  <div class="planner-wrapper">
    <div class="planner">
      <PlannerHeaderVue 
        v-model="isSidebarOpened"
        :currentMonth="currentMonth"
        @prevWeek="prevWeekHandler"
        @nextWeek="nextWeekHandler"
      />
      <div class="planner__loader-wrapper" v-if="isLoading">
        <LoaderVue />
      </div>
      <div class="planner__grid-wrapper" v-if="!isLoading">
        <div class="planner__days-header">
          <PlannerDateVue 
            v-for="day in days"
            :key="day.date" 
            :day="day"
          />
        </div>
        
        <PlannerGrid
          :days="days"
        />
      </div>
      
    </div>
    <RightSidebarVue v-if="userData"
      :isOpened="isSidebarOpened"
    />
  </div>
  
  
</template>

<style lang="scss">
  .planner-wrapper {
    display: flex;
    overflow: hidden;
  }

  .planner {
    height: 100%;
    display: grid;
    grid-template-rows: auto 1fr;
    overflow: hidden;
    flex-grow: 1;

    &__loader-wrapper {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      height: 100%;
    }

    &__grid-wrapper {
      padding-left: size(79px);
      height: 100%;
      position: relative;
      overflow-y: scroll;
    }

    &__days-header {
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      position: sticky;
      top: 0;
      left: 0;
      z-index: 100;
      padding-left: size(79px);
      margin-left: size(-79px);
      background-color: $white;
    }
  }
</style>
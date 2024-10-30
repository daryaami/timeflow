<script setup>
import { ref, onMounted, nextTick, computed, watch } from 'vue';
import { userData } from '@/components/js/data/userData';
import { isSameDay } from '@/components/js/time-utils';
import { getCurrentWeekMonday } from '@/components/js/time-utils';

import PlannerGrid from '@/components/blocks/planner/PlannerGrid.vue';

import PlannerHeaderVue from '../components/blocks/planner/PlannerHeader.vue';
import LoaderVue from '../components/blocks/loaders/Loader.vue';
import EventInfoSidebar from '@/components/blocks/planner/EventInfoSidebar.vue';

import { events } from '@/store/events';

import PlannerDateVue from '../components/blocks/planner/PlannerDate.vue';
import RightSidebarVue from '@/components/blocks/planner/RightSidebar.vue';

const isSidebarOpened = ref(true);
const days = ref([])

// Get events

const isLoading = ref(true);

const createOverlappingCards = (cards) => {
  const sortedCards = cards.sort((a, b) => new Date(a.start) - new Date(b.start))

  for(let i = 1; i < sortedCards.length; i++) {
    const currentCard = sortedCards[i];
    const currentCardStartDate = new Date(currentCard.start);

    for(let j = i - 1; j >= 0; j--) {
      const compCard = sortedCards[j]
      if (currentCardStartDate > new Date(compCard.start) && currentCardStartDate < new Date(compCard.end)) {
        compCard.overlapLevel? 
          currentCard.overlapLevel = compCard.overlapLevel + 1:
          currentCard.overlapLevel = 1;
        
        break;
      }
    }
  }
  
  return sortedCards
}



const createDays = (date, events) => {
  const monday = getCurrentWeekMonday(date)

  days.value = [];
  for (let i = 0; i < 7; i++) {
    const day = new Date(monday);
    day.setDate(monday.getDate() + i); 

    days.value.push({
      weekday: day.toLocaleDateString('en-EN', { weekday: 'short' }),
      date: day.getDate(),
      isToday: isSameDay(day, new Date()),
      day: day,
      cards: [],
    });
  }

  events.forEach(event => {
    const startDate = new Date(event.start.dateTime);
    const endDate = new Date(event.end.dateTime);

    if (startDate.getDate() === endDate.getDate()) {
      const day = days.value.find(day => day.date === startDate.getDate());

      const card = {
        event: event,
        start: event.start.dateTime,
        end: event.end.dateTime,
      }

      day.cards.push(card);
    } else {
      const firstCard = {
        event: event,
        start: event.start.dateTime,
        end: event.start.dateTime.replace(/T\d{2}:\d{2}:\d{2}/, "T23:59:00"),
      }

      const firstDay = days.value.find(day => day.date === startDate.getDate());

      firstDay.cards.push(firstCard);


      const secondCard = {
        event: event,
        start: event.end.dateTime.replace(/T\d{2}:\d{2}:\d{2}/, "T00:00:00"),
        end: event.end.dateTime,
      }

      const secondDay = days.value.find(day => day.date === endDate.getDate());

      secondDay.cards.push(secondCard);
    }
  })
  
  days.value.forEach(day => day.cards = createOverlappingCards(day.cards))
}

const fetchData = async (date = new Date()) => {
  try {
    const fetchedEvents = await events.get(date);
    createDays(date, fetchedEvents)
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

// 



// SelectedEvent

const selectedEvent = ref(null);

const eventClickHandler = (event) => {
  selectedEvent.value = event;
}
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
          :selectedEvent="selectedEvent"
          @event-click="eventClickHandler"
        />
      </div>
      
    </div>
    <div class="planner__right-sidebar"
      v-if="userData"

      :class="{
        'hidden': !isSidebarOpened,
      }"
    >
      <RightSidebarVue 
        v-if="!selectedEvent"
      />

      <EventInfoSidebar
        v-if="selectedEvent"
        :event="selectedEvent"
        @close="selectedEvent = null"
      />
    </div>
    
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

    &__right-sidebar {
      width: size(380px);
      height: 100%;
      transition: .15s;
      overflow: hidden;

      &.hidden {
        width: size(0px);
      }
    }
  }
</style>
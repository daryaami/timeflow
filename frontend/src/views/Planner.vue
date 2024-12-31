<script setup>
import { ref, onMounted, nextTick, computed, watch } from 'vue';
import { userData } from '@/components/js/data/userData';
import { getCurrentWeekMonday } from '@/components/js/time-utils';

import PlannerGrid from '@/components/blocks/planner/PlannerGrid.vue';

import PlannerHeaderVue from '../components/blocks/planner/PlannerHeader.vue';
import LoaderVue from '../components/blocks/loaders/Loader.vue';
import EventInfoSidebar from '@/components/blocks/planner/EventInfoSidebar.vue';

import { events } from '@/store/events';

import RightSidebarVue from '@/components/blocks/planner/RightSidebar.vue';
import { useCurrentDateStore } from '@/store/currentDate';

const isSidebarOpened = ref(true);
const currentEvents = ref();

const currentDate = useCurrentDateStore()

// Get events

const isLoading = ref(true);

const fetchData = async (date) => {
  isLoading.value = true;

  const monday = getCurrentWeekMonday(date)

  try {
    const fetchedEvents = await events.get(monday);
    currentEvents.value = fetchedEvents;
  } catch (error) {
    console.error('ошибка', error);
  } finally {
    isLoading.value = false;
    await nextTick();
  }
}

const nextWeekHandler = async () => {
  if (isLoading.value) return
  currentDate.toNextWeek()
}

const prevWeekHandler = async () => {
  if (isLoading.value) return
  currentDate.toPrevWeek()
}

watch(currentDate, (newVal) => {
  fetchData(newVal.date)
})


// Current Month

const currentMonth = computed(() => {
  if (currentDate.date) {
    const now = currentDate.date;
    return `${now.toLocaleString('default', { month: 'long' })} ${now.getFullYear()}`;
  } else {
    return ''
  }
})

onMounted(() => {
  fetchData(currentDate.date);
})
// 

// SelectedEvent

const selectedEvent = ref(null);

const cardClickHandler = (event) => {
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
        
        
        <PlannerGrid
          v-if="!isLoading"

          :events="currentEvents"
          :current-date="currentDate.date"
          :selectedEvent="selectedEvent"
          @card-click="cardClickHandler"
        />
      
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
    flex-grow: 1;
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
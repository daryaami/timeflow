<script setup>
import { ref, onMounted, nextTick, computed, watch } from 'vue';
import { userData } from '@/components/js/data/userData';
import { getCurrentWeekMonday } from '@/components/js/time-utils';

import PlannerGrid from '@/components/blocks/planner/PlannerGrid.vue';

import PlannerHeaderVue from '../components/blocks/planner/PlannerHeader.vue';
import LoaderVue from '../components/blocks/loaders/Loader.vue';
import EventInfoSidebar from '@/components/blocks/planner/EventInfoSidebar.vue';

import { currentDate } from '@/store/currentDate';
import { events, eventBus } from '@/store/events';

import RightSidebarVue from '@/components/blocks/planner/RightSidebar.vue';

const isSidebarOpened = ref(true);
const currentEvents = ref();

// Get events

const isLoading = ref(true);

const fetchData = async (date = new Date()) => {
  try {
    const fetchedEvents = await events.get(date);
    currentEvents.value = fetchedEvents;
    currentDate.value = date;
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
  
  const date = currentDate.value;
  const nextMonday = getCurrentWeekMonday(new Date(date.setDate(date.getDate() + 7)));

  fetchData(nextMonday);
}

const prevWeekHandler = async () => {
  if (isLoading.value) return
  isLoading.value = true;
  const date = currentDate.value;
  const prevMonday = getCurrentWeekMonday(new Date(date.setDate(date.getDate() - 7)));
  fetchData(prevMonday);
}

watch(eventBus, (newVal) => {
  if (newVal) {
    fetchData(currentDate.value);
  }
});

// Current Month

const currentMonth = computed(() => {
  if (currentDate.value) {
    const now = currentDate.value;
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
          :current-date="currentDate"
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
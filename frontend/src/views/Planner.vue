<script setup>
import { ref, onMounted, nextTick, computed, watch } from 'vue';

import PlannerGrid from '@/components/blocks/planner/PlannerGrid.vue';
import PlannerHeaderVue from '../components/blocks/planner/PlannerHeader.vue';
import LoaderVue from '../components/blocks/loaders/Loader.vue';
import EventInfoSidebar from '@/components/blocks/planner/EventInfoSidebar.vue';

import { useEventsStore } from '@/store/events';

import RightSidebarVue from '@/components/blocks/planner/RightSidebar.vue';
import { useCurrentDateStore } from '@/store/currentDate';

const isSidebarOpened = ref(true);
const currentEvents = ref();

const eventsStore = useEventsStore()

const currentDate = useCurrentDateStore()

// Get events

const isLoading = ref(true);

const fetchData = async (date) => {
  isLoading.value = true;

  try {
    const fetchedEvents = await eventsStore.getEvents(date);
    currentEvents.value = fetchedEvents;
  } catch (error) {
    console.error('ошибка', error);
  } finally {
    isLoading.value = false;
    await nextTick();
  }
}

watch(currentDate, (newVal) => {
  fetchData(newVal.date)
})

watch(eventsStore, () => {
  fetchData(currentDate.date)
})

onMounted(() => {
  fetchData(currentDate.date);
})

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
        :isLoading="isLoading"
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
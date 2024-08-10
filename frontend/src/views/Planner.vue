<script setup>
import { ref, onMounted, nextTick, computed, watch } from 'vue';
import { getPrevWeekEvents, getNextWeekEvents } from '@/components/js/data/events';
import { userData } from '@/components/js/data/userData';

import PlannerGrid from '@/components/blocks/planner/PlannerGrid.vue';

import PlannerHeaderVue from '../components/blocks/planner/PlannerHeader.vue';
import LoaderVue from '../components/blocks/Loader.vue';

import { getEvents } from '@/components/js/data/events';

import PlannerDateVue from '../components/blocks/planner/PlannerDate.vue';
import RightSidebarVue from '@/components/blocks/planner/RightSidebar.vue';

const isSidebarOpened = ref(true);
const currentWeekEvents = ref(null)

// Get events

const isLoading = ref(true);

const fetchData = async () => {
  try {
    currentWeekEvents.value = await getEvents();
  } catch (error) {
    console.error('ошибка', error);
  } finally {
    isLoading.value = false;
  }
}

const nextWeekHandler = async () => {
  if (isLoading.value) return
  isLoading.value = true;
  
  const newEvents = await getNextWeekEvents(currentWeekEvents.value.mon.date);

  currentWeekEvents.value = newEvents;
  isLoading.value = false;
  await nextTick();
  timeLineEl.value.scrollIntoView({ block: "center" });
}

const prevWeekHandler = async () => {
  if (isLoading.value) return
  isLoading.value = true;
  
  const newEvents = await getPrevWeekEvents(currentWeekEvents.value.mon.date);

  currentWeekEvents.value = newEvents;
  isLoading.value = false;
  await nextTick();
  timeLineEl.value.scrollIntoView({ block: "center" });
}

// Current Month

const currentMonth = computed(() => {
  if (currentWeekEvents.value) {
    const now = new Date(currentWeekEvents.value.mon.date);
    return `${now.toLocaleString('default', { month: 'long' })} ${now.getFullYear()}`;
  } else {
    return ''
  }
})

onMounted(() => {
  fetchData();
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
            v-for="day in currentWeekEvents"
            :key="day.date" 
            :date="day.date"
          />
        </div>
        
        <PlannerGrid
          :currentWeekEvents="currentWeekEvents"
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
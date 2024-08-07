<script setup>
import { ref, onMounted, nextTick, computed, watch } from 'vue';
import { getPrevWeekEvents, getNextWeekEvents, events } from '@/components/js/data/events';
import { userData } from '@/components/js/data/userData';

import PlannerHeaderVue from '../components/blocks/planner/PlannerHeader.vue';
import LoaderVue from '../components/blocks/Loader.vue';
import EventCardVue from '../components/blocks/planner/EventCard.vue';
import { getEvents } from '@/components/js/data/events';
import { getStringTime, getDecimalHours } from '@/components/js/time-utils';
import PlannerDateVue from '../components/blocks/planner/PlannerDate.vue';
import RightSidebarVue from '@/components/blocks/planner/RightSidebar.vue';

const isSidebarOpened = ref(true);
const currentWeekEvents = ref(null)

// Current time line 

const timeLineEl = ref(null);

const nowTimeLine = ref({
  caption: '',
  styleTop: '',
})

const updateTimeLine = () => {
  const now = new Date();

  nowTimeLine.value.caption = getStringTime(now);
  nowTimeLine.value.styleTop = `${getDecimalHours(now) * 100 / 24}%`
}

const setTimeLineUpdate =  async () => {
  updateTimeLine();

  await nextTick();

  timeLineEl.value.scrollIntoView({ block: "center" });

  const now = new Date();
  const nextMinute = (60 - now.getSeconds()) * 1000;

  setTimeout(() => {
    updateTimeLine();
    setInterval(updateTimeLine, 60000);
  }, nextMinute)
}


// Get events

const isLoading = ref(true);

const fetchData = async () => {
  try {
    currentWeekEvents.value = await getEvents();
  } catch (error) {
    console.error('ошибка', error);
  } finally {
    isLoading.value = false;
    setTimeLineUpdate();
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




const lines = [
  {
    time: '01:00',
    percent: 100 / 24,
  },
  {
    time: '02:00',
    percent: 200 / 24,
  },
  {
    time: '03:00',
    percent: 300 / 24,
  },
  {
    time: '04:00',
    percent: 400 / 24,
  },
  {
    time: '05:00',
    percent: 500 / 24,
  },
  {
    time: '06:00',
    percent: 600 / 24,
  },
  {
    time: '07:00',
    percent: 700 / 24,
  },
  {
    time: '08:00',
    percent: 800 / 24,
  },
  {
    time: '09:00',
    percent: 900 / 24,
  },
  {
    time: '10:00',
    percent: 1000 / 24,
  },
  {
    time: '11:00',
    percent: 1100 / 24,
  },
  {
    time: '12:00',
    percent: 1200 / 24,
  },
  {
    time: '13:00',
    percent: 1300 / 24,
  },
  {
    time: '14:00',
    percent: 1400 / 24,
  },
  {
    time: '15:00',
    percent: 1500 / 24,
  },
  {
    time: '16:00',
    percent: 1600 / 24,
  },
  {
    time: '17:00',
    percent: 1700 / 24,
  },
  {
    time: '18:00',
    percent: 1800 / 24,
  },
  {
    time: '19:00',
    percent: 1900 / 24,
  },
  {
    time: '20:00',
    percent: 2000 / 24,
  },
  {
    time: '21:00',
    percent: 2100 / 24,
  },
  {
    time: '22:00',
    percent: 2200 / 24,
  },
  {
    time: '23:00',
    percent: 2300 / 24,
  },
]

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
        <div class="planner__grid">
          <div class="planner__day-column"
            v-for="day in currentWeekEvents"
            :key="day.date"  
          >
            <EventCardVue 
              v-for="event, i in day.events"
              :key="i"
              :event="event"
            />
          </div>
          <div class="planner__line"
            v-for="(line, i) in lines"
            :key="i"
            :style="{ top: `${line.percent}%` }"
          >
            <div class="planner__line-time">{{ line.time }}</div>
          </div>

          <div class="planner__line planner__line--now"
            :style="{ top: `${nowTimeLine.styleTop}` }"
            ref="timeLineEl"
          >
            <div class="planner__line-time">{{ nowTimeLine.caption }}</div>
          </div>
        </div>
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

    &__grid {
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      height: size($day-height);
      position: relative;
    }

    &__day-column {
      border-left: 1px solid $dark-lines;
      height: 100%;
      position: relative;
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

    &__line {
      position: absolute;
      left: size(-7px);
      width: calc(100% + size(7px));
      height: 1px;
      background-color: $light-lines;

      &--now {
        background-color: $light-grey;

        & .planner__line-time {
          color: $basic-dark;
        }
      }
    }

    &__line-time {
      @include bold-16;
      position: absolute;
      left: size(-10px);
      top: 0;
      transform: translate(-100%, -100%);
      color: $light-grey;
      background: $white;
    }
  }
</style>
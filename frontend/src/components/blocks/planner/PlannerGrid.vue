<script setup>
import { ref, nextTick, onMounted } from 'vue';
import EventCardVue from './EventCard.vue';
import { getStringTime, getDecimalHours } from '@/components/js/time-utils';

const props = defineProps(['currentWeekEvents'])

// Grid Height
const grid = ref(null)
const gridHeight = ref();

// Current time line 

const timeLineEl = ref(null);
const todayLine = ref(null)

const nowTimeLine = ref({
  caption: '',
  styleTop: '',
})

const updateTodayLine = () => {
  const todayDate = document.querySelector('.planner-date.current');

  if (!todayDate) return

  const position = (todayDate.getBoundingClientRect().left - timeLineEl.value.getBoundingClientRect().left) / timeLineEl.value.offsetWidth * 100
  const width = (todayDate.offsetWidth * .9) / timeLineEl.value.offsetWidth * 100

  todayLine.value.style.left = `${position}%`;
  todayLine.value.style.width = `${width}%`;
}

const updateTimeLine = () => {
  const now = new Date();

  nowTimeLine.value.caption = getStringTime(now);
  nowTimeLine.value.styleTop = `${getDecimalHours(now) * 100 / 24}%`
}

const setTimeLineUpdate =  async () => {
  updateTimeLine();

  await nextTick();

  updateTodayLine();
  timeLineEl.value.scrollIntoView({ block: "center" });

  const now = new Date();
  const nextMinute = (60 - now.getSeconds()) * 1000;

  setTimeout(() => {
    updateTimeLine();
    setInterval(updateTimeLine, 60000);
  }, nextMinute)
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

onMounted(async () => {
  await nextTick();
  setTimeLineUpdate();
  gridHeight.value = grid.value.offsetHeight;
})
</script>

<template>
  <div class="planner__grid"
    ref="grid"
  >
    <div class="planner__day-column"
      v-for="day in currentWeekEvents"
      :key="day.date"  
    >
      <EventCardVue 
        v-for="event, i in day.events"
        :key="i"
        :event="event"
        :gridHeight="gridHeight"
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
      <div class="planner__line-today-line"
        ref="todayLine" 
      ></div>
    </div>
  </div>  
</template>

<style lang="scss">
.planner {
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

    &__line-today-line {
      position: absolute;
      display: block;
      width: 100px;
      left: 50px;
      bottom: 0;
      height: size(2px);
      background-color: #E50F0F;

      &::before {
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translate(-50%, -50%);
        width: size(12px);
        height: size(12px);
        background-color: #E50F0F;
        border-radius: 50%;
      }
    }
}
</style>
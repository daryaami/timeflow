<script setup>
import { ref, nextTick, onMounted, defineEmits, computed } from 'vue';
import EventCardVue from './EventCard.vue';
import { getStringTime, getDecimalHours, getCurrentWeekMonday, isSameDay } from '@/components/js/time-utils';
import { lines } from '@/components/js/data/lines';

const props = defineProps(['events', 'currentDate',  'selectedEvent'])
import PlannerDateVue from './PlannerDate.vue';
const emit = defineEmits(['cardClick']);


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

const days = computed(() => {
  const monday = getCurrentWeekMonday(props.currentDate)

  const days = [];
  for (let i = 0; i < 7; i++) {
    const day = new Date(monday);
    day.setDate(monday.getDate() + i); 

    days.push({
      weekday: day.toLocaleDateString('en-EN', { weekday: 'short' }),
      date: day.getDate(),
      isToday: isSameDay(day, new Date()),
      day: day,
      cards: [],
    });
  }

  props.events.forEach(event => {
    const startDate = new Date(event.start.dateTime);
    const endDate = new Date(event.end.dateTime);

    if (startDate.getDate() === endDate.getDate()) {
      const day = days.find(day => day.date === startDate.getDate());

      if (!day) return;

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

      const firstDay = days.find(day => day.date === startDate.getDate());

    

      if (firstDay)  firstDay.cards.push(firstCard);


      const secondCard = {
        event: event,
        start: event.end.dateTime.replace(/T\d{2}:\d{2}:\d{2}/, "T00:00:00"),
        end: event.end.dateTime,
      }

      const secondDay = days.find(day => day.date === endDate.getDate());

      if (firstDay) secondDay.cards.push(secondCard);
    }
  })
  
  days.forEach(day => day.cards = createOverlappingCards(day.cards))

  return days
}) 


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
  todayLine.value.style.display = 'none';
  const todayDate = document.querySelector('.planner-date.current');

  if (!todayDate) return

  const position = (todayDate.getBoundingClientRect().left - timeLineEl.value.getBoundingClientRect().left) / timeLineEl.value.offsetWidth * 100
  const width = (todayDate.offsetWidth * .9) / timeLineEl.value.offsetWidth * 100

  todayLine.value.style.left = `${position}%`;
  todayLine.value.style.width = `${width}%`;
  todayLine.value.style.display = 'block';
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

onMounted(async () => {
  await nextTick();
  setTimeLineUpdate();
  gridHeight.value = grid.value.offsetHeight;
})
</script>

<template>
  <div class="planner__grid-wrapper" >

    <div class="planner__days-header">
      <PlannerDateVue 
        v-for="day in days"
        :key="day.date" 
        :day="day"
      />
    </div>

    <div class="planner__grid"
      ref="grid"
    >
      <div class="planner__day-column"
        v-for="day in days"
        :key="day.date"  
      >
        <EventCardVue 
          v-for="card, i in day.cards"
          :key="i"
          :card="card"
          :gridHeight="gridHeight"
          @click=" emit('cardClick', card.event)"
          :class="{
            'selected': selectedEvent === card.event,
          }"
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
      pointer-events: none;

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
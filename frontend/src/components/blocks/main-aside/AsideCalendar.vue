<script setup>
import { currentDate } from '@/store/currentDate';
import { ref, computed, watch } from 'vue';
import { getCurrentWeekMonday, getTomorrow } from '@/components/js/time-utils';

const weekDays = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];

const currentCalendarDate = ref(new Date(currentDate.value));


const days = computed(() => {
  const daysArr = []

  let firstDayofMonth;
  let firstDay;

  firstDayofMonth = new Date(currentCalendarDate.value);
  firstDayofMonth = new Date(firstDayofMonth.setDate(1));

  firstDay = getCurrentWeekMonday(firstDayofMonth);

  daysArr.push(firstDay)

  for(let i = 0; i < 34; i++) {
    const newDay = getTomorrow(daysArr[i]);
    daysArr.push(newDay);
  }

  return daysArr
})

const currentMonth = computed(() => {
  return `${currentCalendarDate.value.toLocaleString('default', { month: 'long' })} ${currentCalendarDate.value.getFullYear()}`;
})

const nextMonthHandler = () => {
  currentCalendarDate.value = new Date(currentCalendarDate.value.setMonth(currentCalendarDate.value.getMonth() + 1)) 
}

const prevMonthHandler = () => {
  currentCalendarDate.value = new Date(currentCalendarDate.value.setMonth(currentCalendarDate.value.getMonth() - 1)) 
}

watch(currentDate, (newValue) => {
  currentCalendarDate.value = newValue;
})

</script>

<template>
  <div class="aside-calendar">
    <div class="aside-calendar__wrapper">
      <div class="aside-calendar__month-wrapper">
        <span class="aside-calendar__month">{{ currentMonth }}</span>
        <div class="aside-calendar__buttons-wrapper">
          <button class="aside-calendar__button"
            @click="prevMonthHandler"
          >
            <svg width="16" height="16">
              <use xlink:href="#arrow-prev"/>
            </svg>
          </button>

          <button class="aside-calendar__button"
            @click="nextMonthHandler"
          >
            <svg width="16" height="16">
              <use xlink:href="#arrow-next"/>
            </svg>
          </button>
        </div>
      </div>

      <div class="aside-calendar__header aside-calendar__grid">
        <span class="aside-calendar__weekday aside-calendar__day"
          v-for="weekDay, i in weekDays"
          :key="i"
        >
          {{ weekDay }}
        </span>
      </div>

      <div class="aside-calendar__calendar aside-calendar__grid">
        <button class="aside-calendar__day aside-calendar__date"
          v-for="day, i in days"
          :key="i"
          :class="{'aside-calendar__date--uncurrent': day.getMonth() != currentCalendarDate.getMonth() }"
          @click="currentDate = day"
        >
            {{ day.getDate() }}
      </button>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
.aside-calendar {
  padding-left: size(46px);
  margin-bottom: size(70px);

  &__wrapper {
    width: fit-content;
  }

  &__month-wrapper {
    margin-bottom: size(32px);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  &__month {
    @include bold-18;
  }

  &__grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    column-gap: size(11px);
    row-gap: size(10px);
  }

  &__header {
    width: fit-content;
  }

  &__weekday {
    @include bold-18;
    color: $light-grey;
  }

  &__calendar {
    width: fit-content;
  }

  &__day {
    display: flex;
    align-items: center;
    justify-content: center;
    @include bold-18;
    width: size(26px);
    height: size(26px);
  }

  &__date {
    @include reset-button;
    background-color: $white;
    border-radius: 50%;

    &--uncurrent {
      background: transparent;
      color: $dark-grey;
    }
  }

  &__buttons-wrapper {
    display: flex;
    align-items: center;
    gap: size(18px);
  }

  &__button {
    @include reset-button;
    display: flex;
    align-items: center;
    justify-content: center;
    width: size(16px);
    height: size(16px);

    & svg {
      display: block;
      width: 100%;
      height: 100%;
    }
  }
}
</style>
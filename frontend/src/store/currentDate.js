import { defineStore } from "pinia";
import { ref } from 'vue'

import { getCurrentWeekMonday } from '@/components/js/time-utils';

export const useCurrentDateStore = defineStore("currentDate", () => {
  const date = ref(new Date())

  const toNextWeek = () => {
    const newDate = date.value;
    const nextMonday = getCurrentWeekMonday(new Date(newDate.setDate(newDate.getDate() + 7)));
    date.value = nextMonday
  }

  const toPrevWeek = () => {
    const newDate = date.value;
    const prevMonday = getCurrentWeekMonday(new Date(newDate.setDate(newDate.getDate() - 7)));
    date.value = prevMonday
  }

  const setDate = (newDate) => {
    date.value = newDate
  }

  return { 
    date,
    toNextWeek,
    toPrevWeek,
    setDate,
  }
})
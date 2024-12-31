import { defineStore } from "pinia";
import { ref } from 'vue';
import { getCurrentWeekMonday, getStringDate, isSameDay } from '@/components/js/time-utils';


export const useEventsStore = defineStore("events", () => {
  const events = ref([]);
  const loadedMondays = [];

  const getEvents = async (date = new Date()) => {
    const monday = getCurrentWeekMonday(date)

    if (loadedMondays.filter(item => isSameDay(monday, item)).length) {
      return events.value
    }

    let response = await fetch(`${window.location.origin}/planner_api/get_events/?date=${getStringDate(monday)}`);

    if (response.ok) {
      const data = await response.json();
      events.value = [...events.value, ...data.events].reduce((acc, current) => {
        const x = acc.find(item => item.id === current.id);
        if (!x) {
          acc.push(current);
        }
        return acc;
      }, [])

      loadedMondays.push(monday);
      return data.events;
    } else {
      throw new Error('Failed to fetch events');
    }
  }

  const update = (newEvents) => {
    events.value = [...events.value, ...newEvents];
  }

  return {
    events,
    loadedMondays,
    getEvents,
    update,
  }
})


import { ref } from 'vue';
import { getCurrentWeekMonday, getStringDate, isSameDay } from '../time-utils';

let events = [];
const loadedMondays = [];
const updatedEvents = ref([])

const getEvents = async (date = new Date()) => {
  if (loadedMondays.filter(item => isSameDay(date, item)).length) {
    return events;
  }

  let response = await fetch(`${window.location.origin}/planner_api/get_events?date=${getStringDate(date)}`);
  if (response.ok) {
    const data = await response.json();
    events = [...events, ...data.events].reduce((acc, current) => {
      const x = acc.find(item => item.id === current.id);
      if (!x) {
        acc.push(current);
      }
      return acc;
    }, [])



    let loadedDay;
    date === ''?  loadedDay = new Date(): loadedDay = new Date(date);
    const loadedMonday = getCurrentWeekMonday(loadedDay);
    loadedMondays.push(loadedMonday);
    return data.events;
  } else {
    throw new Error('Failed to fetch events');
  }
}

const updateEvents = (newEvents) => {
  events = [...events, ...newEvents];
  updatedEvents.value = newEvents;
}


export { updateEvents, updatedEvents, getEvents}
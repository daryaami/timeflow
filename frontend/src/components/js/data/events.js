import { ref } from 'vue';
import { getStringDate } from '../time-utils';

const events = ref([]);
const loadedMondays = [];

const getEvents = async (date = '') => {
  // date в формате '2024-06-24'

  // TODO
  // Вычислить понедельник
  // Если понедельник загружен, вернуть события 

  let response = await fetch(`${window.location.origin}/planner_api/get_events${date? '?date=' + date: ''}`);
  if (response.ok) {
    const data = await response.json();
    events.value.push(data.events);

    let loadedDay;
    date === ''?  loadedDay = new Date(): loadedDay = new Date(date);
    const loadedMonday = new Date(loadedDay.setDate(loadedDay.getDate() - loadedDay.getDay() + 1));
    loadedMondays.push(getStringDate(loadedMonday))
    console.log(loadedMondays)
    return data.events;
  } else {
    throw new Error('Failed to fetch events');
  }
}

const updateEvents = (newEvents) => {
  // TODO
  // Переделать

  const updatedEvents = { ...events.value }; 

  newEvents.forEach(event => {
    const eventDate = getStringDate(event.start.dateTime);
    
    for (const day in updatedEvents) {
      if (updatedEvents[day].date === eventDate) {
        updatedEvents[day].events.push(event)
      }
    }
  });

  events.value = updatedEvents;
}


export { events, updateEvents, getEvents}
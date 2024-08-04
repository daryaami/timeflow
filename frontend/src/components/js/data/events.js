import { ref } from 'vue';
import { getStringDate } from '../time-utils';

const events = ref([]);

const getEvents = async (date = '') => {
  // date в формате '2024-06-24'

  let response = await fetch(`${window.location.origin}/planner_api/get_events${date? '?date=' + date: ''}`);
  if (response.ok) {
    const data = await response.json();
    events.value.push(data.days);
    return data.days;
  } else {
    throw new Error('Failed to fetch events');
  }
}

const updateEvents = (newEvents) => {
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

const getNextWeekEvents = async (date) => {
  const currentDate = new Date(date);
  console.log(currentDate);

  const nextMonday = new Date(currentDate);
  
  nextMonday.setDate(currentDate.getDate() + 7);
  
  const newEvents = await getEvents(getStringDate(nextMonday))

  events.value.push(newEvents);

  return newEvents
};

const getPrevWeekEvents = async (date) => {
  const currentDate = new Date(date);
  const prevMonday = new Date(currentDate);
  prevMonday.setDate(currentDate.getDate() - 7);

  const prevMondayString = getStringDate(prevMonday)

  const findedEvents = events.value.find(el => el.mon.date === prevMondayString)

  if (findedEvents) {
    return findedEvents;
  }
  
  const newEvents = await getEvents(prevMonday)

  events.value.push(newEvents);

  return newEvents
};


export { events, updateEvents, getEvents, getNextWeekEvents, getPrevWeekEvents }
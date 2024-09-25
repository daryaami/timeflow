import { getCurrentWeekMonday, getStringDate, isSameDay } from '../time-utils';

let events = [];
const loadedMondays = [];

const getEvents = async (date = new Date()) => {
  if (loadedMondays.filter(item => isSameDay(date, item)).length) {
    return events;
  }

  let response = await fetch(`${window.location.origin}/planner_api/get_events?date=${getStringDate(date)}`);
  if (response.ok) {
    const data = await response.json();
    events = [...events, ...data.events];

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
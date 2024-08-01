import { ref } from 'vue';
import { getStringDate } from '../time-utils';

const events = ref({});

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


export { events, updateEvents }
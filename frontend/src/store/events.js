import { reactive} from 'vue';
import { getCurrentWeekMonday, getStringDate, isSameDay } from '@/components/js/time-utils';
// const updatedEvents = ref([])

const events = reactive({
  list: [],
  loadedMondays: [],
  async get(date = new Date()) {
    if (this.loadedMondays.filter(item => isSameDay(date, item)).length) {
      return events;
    }

    let response = await fetch(`${window.location.origin}/planner_api/get_events?date=${getStringDate(date)}`);
    if (response.ok) {
      const data = await response.json();
      this.list = [...this.list, ...data.events].reduce((acc, current) => {
        const x = acc.find(item => item.id === current.id);
        if (!x) {
          acc.push(current);
        }
        return acc;
      }, [])

      const loadedMonday = getCurrentWeekMonday(date);
      this.loadedMondays.push(loadedMonday);
      return data.events;
    } else {
      throw new Error('Failed to fetch events');
    }
  }
})


const updateEvents = (newEvents) => {
  // events = [...events, ...newEvents];
  // updatedEvents.value = newEvents;
}


export { events, updateEvents, }
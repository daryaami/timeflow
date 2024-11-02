import { reactive, ref } from 'vue';
import { getCurrentWeekMonday, getStringDate, isSameDay } from '@/components/js/time-utils';

const eventBus = ref({})

const events = reactive({
  _list: [],
  loadedMondays: [],
  async get(date = new Date()) {

    if (this.loadedMondays.filter(item => isSameDay(date, item)).length) {
      return this._list;
    }

    let response = await fetch(`${window.location.origin}/planner_api/get_events?date=${getStringDate(date)}`);

    if (response.ok) {
      const data = await response.json();
      this._list = [...this._list, ...data.events].reduce((acc, current) => {
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
  },

  update(newEvents) {
    this._list = [...this._list, ...newEvents];
    eventBus.value = true;
    setTimeout(() => eventBus.value = false, 1000);
  }
})


export { events, eventBus }
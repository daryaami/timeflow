<script setup>
import { ref, onMounted } from 'vue';
import PlannerHeaderVue from '../components/blocks/planner/PlannerHeader.vue';
import LoaderVue from '../components/blocks/Loader.vue';

const events = ref();
const isLoading = ref(true);

const fetchData = async () => {
  let response = await fetch(`${window.location.origin}/planner/get_events/`);

  if (response.ok) {
    let json = await response.json();
    events.value = json.days;
    isLoading.value = false;
  } else {
    throw new Error()
  }
}

try {
  fetchData()
} catch (error) {
  console.log('ошибка')
}
</script>

<template>
  <div class="planner">
    <PlannerHeaderVue />
    <div class="planner__loader-wrapper" v-if="isLoading">
      <LoaderVue />
    </div>
    <div class="planner__grid" v-if="!isLoading">
      <div 
        v-for="day in events"
        :key="day.date"  
      >
        <h3>{{ day.date }}</h3>
        <ul v-if="day.events">
          <li 
            v-for="event, i in day.events"
            :key="i"
          >
            {{ event.summary }}
          </li>
        </ul>
      </div>
    </div>
    
  </div>
  
  
</template>

<style lang="scss">
  .planner {
    display: flex;
    flex-direction: column;
    height: 100%;

    &__loader-wrapper {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      height: 100%;
    }

    &__grid {
      display: grid;
      grid-template-columns: repeat(7, 1fr);
    }
  }
</style>
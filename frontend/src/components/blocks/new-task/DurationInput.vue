<script setup>
import { ref, watch, onMounted } from 'vue';
import { convertMinToTimeString } from '@/components/js/time-utils';

const props = defineProps(['label', 'buttons', 'isValid', 'errorMessage'])

const duration = defineModel();
const durationString = ref(null)
const forceUpdate = ref(0);

watch([duration, forceUpdate], (newValues) => {
  const newValue = newValues[0];
  durationString.value = convertMinToTimeString(newValue)
});

const increaseDuration = () => {
  if (duration.value < 60) {
    duration.value += 15 - duration.value % 15;
  } else if (duration.value < 120) {
    duration.value += 30 - duration.value % 30;
  } else {
    duration.value += 60 - duration.value % 60;
  }
}

const decreaseDuration = () => {
  if (duration.value <= 15) return

  if (duration.value <= 60) {
    const rem = duration.value % 15;
    rem? duration.value -= rem: duration.value -= 15; 
  } else if (duration.value <= 120) {
    const rem = duration.value % 30;
    rem? duration.value -= rem: duration.value -= 30; 
  } else {
    const rem = duration.value % 60;
    rem? duration.value -= rem: duration.value -= 60; 
  }
}


const extractTime = (text) => {
  const regexFull = /(\d+)\D*hr\D*(\d+)\D*min/;
  const regexHoursOnly = /(\d+)\D*hr/;
  const regexMinutesOnly = /(\d+)\D*min/;

  
  let match = text.match(regexFull);
  if (match) {
    const hours = match[1];
    const mins = match[2];
    return {
      hours,
      mins,    
    }
  }
  
  match = text.match(regexHoursOnly);
  if (match) {
      const hours = match[1];

      return {
        hours,
        mins: 0,    
      }
  }
  
  match = text.match(regexMinutesOnly);
  if (match) {
      const mins = match[1];

      return {
        hours: 0,
        mins,    
      }
  }
  
  return null;
}

const inputBlurHandler = () => {
  const time = extractTime(durationString.value)
  duration.value = Number(time.hours) * 60  + Number(time.mins);
  forceUpdate.value += 1;
}

onMounted(() => forceUpdate.value += 1)
</script>

<template>
<div class="duration-input input">
  <input type="text" class="input__input" 
    :class="{'error': isValid}"
    v-model="durationString"
    @blur="inputBlurHandler"
  >
  <span class="input__label">{{ label }}</span>
  <span class="input__error-message" v-if="isValid">{{ errorMessage }}</span>
  
  <div class="duration-input__buttons" v-if="buttons">
    <button class="duration-input__button duration-input__button--minus"
      @click.prevent="decreaseDuration"
    ></button>

    <button class="duration-input__button duration-input__button--plus"
      @click.prevent="increaseDuration"
    ></button>
  </div>
</div>
</template>

<style lang="scss">
.duration-input {
  &__buttons {
    position: absolute;
    right: size(8px);
    top: 50%;
    transform: translateY(-50%);
    display: flex;
    gap: size(4px);
  }

  &__button {
    @include reset-button;
    display: block;
    background-size: size(20px) size(20px);
    background-position: center;
    width: size(30px);
    height: size(30px);
    border-radius: 50%;
    background-repeat: no-repeat;

    @include hover {
      background-color: $dark-white;
    }


    &--minus {
      background-image: url("data:image/svg+xml,%3Csvg width='20' height='20' viewBox='0 0 20 20' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z' stroke='%233B61E8' stroke-width='2'/%3E%3Cpath d='M7.5 10H12.5' stroke='%233B61E8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E%0A");
    }

    &--plus {
      background-image: url("data:image/svg+xml,%3Csvg width='20' height='20' viewBox='0 0 20 20' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M7.5 10H12.5' stroke='%233B61E8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3Cpath d='M10 7.5V12.5' stroke='%233B61E8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3Cpath d='M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z' stroke='%233B61E8' stroke-width='2'/%3E%3C/svg%3E%0A");
    }
  }
}
</style>
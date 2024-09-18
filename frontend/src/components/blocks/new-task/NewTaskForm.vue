<script setup>
import DurationInputVue from "./DurationInput.vue";
import PrioritySelectVue from "./PrioritySelect.vue";
import CheckboxVue from "../form/Checkbox.vue";
import HoursSelectVue from "./HoursSelect.vue";
import DateInputVue from "./DateInput.vue";
import TextareaVue from "../form/Textarea.vue";
import PrivateCheckbox from "./PrivateCheckbox.vue";
import growHeightTransition from "@/components/transitions/growHeightTransition.vue";

import { computed, ref, watch, defineEmits } from "vue";
import { getTomorrow } from "@/components/js/time-utils";
import { getCookie } from "@/components/js/getCookie";
import { convertMinToTimeString } from "@/components/js/time-utils";
import { updateEvents } from "@/components/js/data/events";


const emit = defineEmits(['successSubmit']);
const isNotes = ref(false);
const isMinDurationrValid = ref(true);

const name = ref();
const priority = ref();
const isSplited = ref(false);
const duration = ref(90);
const minDuration = ref(30);
const maxDuration = ref(90);
const dueDate = ref(getTomorrow().toISOString());
const hours = ref();
const notes = ref(null);
const isPrivate = ref(true)

const isNameFilled = ref(true);


const minDurationErrorMessage = computed(() => {
  return `Max duration is ${convertMinToTimeString(maxDuration.value)}`
})


const validateForm = () => {
  let isFormValid = true;

  if (!name.value) {
    isFormValid = false;
    isNameFilled.value = false;
  } 

  if (minDuration.value > maxDuration.value && isSplited.value) {
    isFormValid = false;
    isMinDurationrValid.value = false;
  }

  return isFormValid
}

const nameInputHandler = () => {
  if (isNameFilled.value) return

  if (name.value) {
    isNameFilled.value = true;
  }
}

const getFormData = () => {
  let data = {
    name: name.value,
    priority: priority.value,
    duration: duration.value,
    hours_id: String(hours.value),
    due_date: dueDate.value,
    private: isPrivate.value,
  }
  
  const durations = {
    min_duration: minDuration.value,
    max_duration: maxDuration.value,
  }

  if (isSplited.value) {
    data = {
      ...data,
      ...durations,
    }
  }

  if (notes.value && isNotes.value) {
    data.notes = notes.value;
  }
  
  return data
}


const submitHandler = async (e) => {
  e.preventDefault();

  if (!validateForm()) return

  const csrftoken = getCookie('csrftoken');
  const formData = getFormData();

  let response;

  try {
    response = await fetch(`${window.location.origin}/task_api/create_task/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=utf-8',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify(formData)
    }).then(data => data.json());
  } catch (error) {
    console.error('ошибка', error);
    return
  }

  updateEvents(response.events);
  emit('successSubmit');
}

watch(minDuration, (newValue) => {
  if (newValue <= maxDuration.value) {
    isMinDurationrValid.value = true;
  }
})

watch(maxDuration, (newValue) => {
  if (minDuration.value <= newValue) {
    isMinDurationrValid.value = true;
  }
})
</script>

<template>
  
    <form class="new-task-form" @submit="submitHandler">
      <div class="new-task-form__row">
        <div class="new-task-form__name-wrapper input">
          <input type="text" 
            class="input__input new-task-form__name-input"
            placeholder="Task name..."
            v-model="name"
            :class="{'error': !isNameFilled}"
            @input="nameInputHandler"
          >
          <span class="input__error-message" v-if="!isNameFilled">Task title is required</span>
        </div>

        <PrioritySelectVue
          v-model="priority"
        />
      </div>

      <div class="new-task-form__row">
        <DurationInputVue
          label="Duration"
          :buttons="true"
          v-model="duration"
        />
        <CheckboxVue 
          class="new-task-form__split-check"
          label="Split up"
          v-model="isSplited"
        />
      </div>
      
      <growHeightTransition>
        <div class="new-task-form__durations" v-if="isSplited">
          <DurationInputVue
            label="Min duration"
            v-model="minDuration"
            :buttons="true"
            :isValid="!isMinDurationrValid"
            :errorMessage = "minDurationErrorMessage"
          />
          <DurationInputVue 
            label="Max duration"
            :buttons="true"
            v-model="maxDuration"
          />
        </div>
      </growHeightTransition>

      <HoursSelectVue
        v-model="hours"
      />

      <div class="new-task-form__row new-task-form__dates">
        <DateInputVue
          label="Schedule after"
        />
        <DateInputVue
          label="Due date"
          v-model="dueDate"
        />
      </div>

      <growHeightTransition>
        <div class="new-task-form__notes-wrapper"
          v-if="isNotes"
        >
          <TextareaVue 
            v-model="notes"
          />
        </div>
      </growHeightTransition>
    

      <div class="new-task-form__row">
        <button class="new-task-form__icon-button"
          @click.prevent="isNotes = !isNotes"
        >
          <svg width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12.5003 5H9.00025C7.60011 5 6.89953 5 6.36475 5.27249C5.89434 5.51216 5.51216 5.89434 5.27249 6.36475C5 6.89953 5 7.60011 5 9.00025V21.0002C5 22.4004 5 23.1001 5.27249 23.6349C5.51216 24.1052 5.89434 24.4881 6.36475 24.7277C6.899 25 7.59874 25 8.99614 25H21.0039C22.4013 25 23.1 25 23.6343 24.7277C24.1046 24.4881 24.4881 24.1049 24.7277 23.6345C25 23.1003 25 22.4013 25 21.0039V17.5M20 6.25L12.5 13.75V17.5H16.25L23.75 10M20 6.25L23.75 2.5L27.5 6.25L23.75 10M20 6.25L23.75 10" stroke="#3B61E8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>

        <PrivateCheckbox
          :class="{'private': isPrivate}"
          v-model="isPrivate"
        />
        
        <button class="new-task-form__button">Create</button>
      </div>
    </form>
</template>

<style lang="scss">
.new-task-form {
  width: size(376px);
  display: flex;
  flex-direction: column;

  &__row {
    display: flex;
    align-items: center;
    width: 100%;

    &:not(:last-child) {
      margin-bottom: size(30px);
    }
  }

  &__name-wrapper {
    position: relative;
    flex-basis: 100%;

    &::before {
      content: '';
      position: absolute;
      left: size(13px);
      top: size(21px);
      transform: translateY(-50%);
      display: block;
      width: size(20px);
      height: size(20px);
      background-image: url("data:image/svg+xml,%3Csvg width='20' height='20' viewBox='0 0 20 20' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M5.625 8.22266C5.625 8.4713 5.72377 8.70975 5.89959 8.88557C6.0754 9.06138 6.31386 9.16016 6.5625 9.16016C6.81114 9.16016 7.0496 9.06138 7.22541 8.88557C7.40123 8.70975 7.5 8.4713 7.5 8.22266C7.5 7.97402 7.40123 7.73556 7.22541 7.55974C7.0496 7.38393 6.81114 7.28516 6.5625 7.28516C6.31386 7.28516 6.0754 7.38393 5.89959 7.55974C5.72377 7.73556 5.625 7.97402 5.625 8.22266ZM12.5 8.22266C12.5 8.4713 12.5988 8.70975 12.7746 8.88557C12.9504 9.06138 13.1889 9.16016 13.4375 9.16016C13.6861 9.16016 13.9246 9.06138 14.1004 8.88557C14.2762 8.70975 14.375 8.4713 14.375 8.22266C14.375 7.97402 14.2762 7.73556 14.1004 7.55974C13.9246 7.38393 13.6861 7.28516 13.4375 7.28516C13.1889 7.28516 12.9504 7.38393 12.7746 7.55974C12.5988 7.73556 12.5 7.97402 12.5 8.22266ZM10 1.25C5.16797 1.25 1.25 5.16797 1.25 10C1.25 14.832 5.16797 18.75 10 18.75C14.832 18.75 18.75 14.832 18.75 10C18.75 5.16797 14.832 1.25 10 1.25ZM15.1367 15.1367C14.4688 15.8047 13.6914 16.3281 12.8262 16.6953C11.9336 17.0742 10.9824 17.2656 10 17.2656C9.01758 17.2656 8.06641 17.0742 7.17188 16.6953C6.30795 16.3305 5.52321 15.8011 4.86133 15.1367C4.19336 14.4688 3.66992 13.6914 3.30273 12.8262C2.92578 11.9336 2.73438 10.9824 2.73438 10C2.73438 9.01758 2.92578 8.06641 3.30469 7.17188C3.66955 6.30795 4.1989 5.52321 4.86328 4.86133C5.53125 4.19336 6.30859 3.66992 7.17383 3.30273C8.06641 2.92578 9.01758 2.73438 10 2.73438C10.9824 2.73438 11.9336 2.92578 12.8281 3.30469C13.692 3.66955 14.4768 4.1989 15.1387 4.86328C15.8066 5.53125 16.3301 6.30859 16.6973 7.17383C17.0742 8.06641 17.2656 9.01758 17.2656 10C17.2656 10.9824 17.0742 11.9336 16.6953 12.8281C16.3309 13.6917 15.8015 14.4759 15.1367 15.1367ZM12.9688 10.4102H12.0293C11.9473 10.4102 11.877 10.4727 11.8711 10.5547C11.7969 11.5215 10.9863 12.2852 10 12.2852C9.01367 12.2852 8.20117 11.5215 8.12891 10.5547C8.12305 10.4727 8.05273 10.4102 7.9707 10.4102H7.03125C7.01006 10.4101 6.98908 10.4144 6.96959 10.4228C6.95011 10.4311 6.93252 10.4433 6.91791 10.4586C6.90329 10.474 6.89195 10.4922 6.88457 10.512C6.8772 10.5319 6.87394 10.5531 6.875 10.5742C6.96094 12.2207 8.33008 13.5352 10 13.5352C11.6699 13.5352 13.0391 12.2207 13.125 10.5742C13.1261 10.5531 13.1228 10.5319 13.1154 10.512C13.108 10.4922 13.0967 10.474 13.0821 10.4586C13.0675 10.4433 13.0499 10.4311 13.0304 10.4228C13.0109 10.4144 12.9899 10.4101 12.9688 10.4102Z' fill='%23858893'/%3E%3C/svg%3E%0A");
      background-size: 100%;
    }

    &:has(:active),
    &:has(:focus),
    &:hover {
      &::before {
        background-image: url("data:image/svg+xml,%3Csvg width='20' height='20' viewBox='0 0 20 20' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M5.625 8.22266C5.625 8.4713 5.72377 8.70975 5.89959 8.88557C6.0754 9.06138 6.31386 9.16016 6.5625 9.16016C6.81114 9.16016 7.0496 9.06138 7.22541 8.88557C7.40123 8.70975 7.5 8.4713 7.5 8.22266C7.5 7.97402 7.40123 7.73556 7.22541 7.55974C7.0496 7.38393 6.81114 7.28516 6.5625 7.28516C6.31386 7.28516 6.0754 7.38393 5.89959 7.55974C5.72377 7.73556 5.625 7.97402 5.625 8.22266ZM12.5 8.22266C12.5 8.4713 12.5988 8.70975 12.7746 8.88557C12.9504 9.06138 13.1889 9.16016 13.4375 9.16016C13.6861 9.16016 13.9246 9.06138 14.1004 8.88557C14.2762 8.70975 14.375 8.4713 14.375 8.22266C14.375 7.97402 14.2762 7.73556 14.1004 7.55974C13.9246 7.38393 13.6861 7.28516 13.4375 7.28516C13.1889 7.28516 12.9504 7.38393 12.7746 7.55974C12.5988 7.73556 12.5 7.97402 12.5 8.22266ZM10 1.25C5.16797 1.25 1.25 5.16797 1.25 10C1.25 14.832 5.16797 18.75 10 18.75C14.832 18.75 18.75 14.832 18.75 10C18.75 5.16797 14.832 1.25 10 1.25ZM15.1367 15.1367C14.4688 15.8047 13.6914 16.3281 12.8262 16.6953C11.9336 17.0742 10.9824 17.2656 10 17.2656C9.01758 17.2656 8.06641 17.0742 7.17188 16.6953C6.30795 16.3305 5.52321 15.8011 4.86133 15.1367C4.19336 14.4688 3.66992 13.6914 3.30273 12.8262C2.92578 11.9336 2.73438 10.9824 2.73438 10C2.73438 9.01758 2.92578 8.06641 3.30469 7.17188C3.66955 6.30795 4.1989 5.52321 4.86328 4.86133C5.53125 4.19336 6.30859 3.66992 7.17383 3.30273C8.06641 2.92578 9.01758 2.73438 10 2.73438C10.9824 2.73438 11.9336 2.92578 12.8281 3.30469C13.692 3.66955 14.4768 4.1989 15.1387 4.86328C15.8066 5.53125 16.3301 6.30859 16.6973 7.17383C17.0742 8.06641 17.2656 9.01758 17.2656 10C17.2656 10.9824 17.0742 11.9336 16.6953 12.8281C16.3309 13.6917 15.8015 14.4759 15.1367 15.1367ZM12.9688 10.4102H12.0293C11.9473 10.4102 11.877 10.4727 11.8711 10.5547C11.7969 11.5215 10.9863 12.2852 10 12.2852C9.01367 12.2852 8.20117 11.5215 8.12891 10.5547C8.12305 10.4727 8.05273 10.4102 7.9707 10.4102H7.03125C7.01006 10.4101 6.98908 10.4144 6.96959 10.4228C6.95011 10.4311 6.93252 10.4433 6.91791 10.4586C6.90329 10.474 6.89195 10.4922 6.88457 10.512C6.8772 10.5319 6.87394 10.5531 6.875 10.5742C6.96094 12.2207 8.33008 13.5352 10 13.5352C11.6699 13.5352 13.0391 12.2207 13.125 10.5742C13.1261 10.5531 13.1228 10.5319 13.1154 10.512C13.108 10.4922 13.0967 10.474 13.0821 10.4586C13.0675 10.4433 13.0499 10.4311 13.0304 10.4228C13.0109 10.4144 12.9899 10.4101 12.9688 10.4102Z' fill='%233b61e8'/%3E%3C/svg%3E%0A");
      }
    }
  }

  &__name-input.input__input {
    padding-left: size(42px);

    &::placeholder {
      color: $light-grey;
    }
  }

  &__button {
    @include reset-button;
    @include bold-18;
    color: $white;
    background: $blue;
    margin-left: auto;
    padding: size(11px) size(14px);
    border-radius: size(30px);
  }

  &__split-check {
    margin-left: size(29px);
  }

  &__durations {
    display: flex;
    gap: size(10px);
  }

  &__dates {
    gap: size(10px);
  }

  &__icon-button {
    @include reset-button;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: size(18px);
  }


  & .active + .hours-select {
    margin-top: size(30px);
  }

  &__notes-wrapper {
    transition: .2s;
    padding-bottom: size(30px);
  }
}
</style>
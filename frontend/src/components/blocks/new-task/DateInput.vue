<script setup>
import VueDatePicker from '@vuepic/vue-datepicker';
const props = defineProps(['label'])

const date = defineModel();

const format = (date) => {
  const day = date.getDate();
  const month = date.getMonth() + 1;
  const year = date.getFullYear();
  const hours = date.getHours();
  const minutes = date.getMinutes();

  return `${day}/${month}/${year} ${hours}:${minutes}`;
}
</script>

<template>
  <div class="date-input input">
    <div class="input__input">
      <VueDatePicker v-model="date"
        text-input
        time-picker-inline
        :clearable="false"
        :min-date="new Date()"
        :day-names="['M', 'T', 'W', 'T', 'F', 'S', 'S']"
        auto-apply
        disable-year-select
        month-name-format="long"
        hide-offset-dates
        hide-input-icon
        model-type="iso"
        placeholder="Now"
        :format="format"
      >
        <template #arrow-left>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M10.8096 2.17852C10.5557 1.94049 10.1442 1.94049 9.89028 2.17852L5.57117 6.22834C4.80981 6.94224 4.80958 8.09957 5.57064 8.81372L9.84159 12.8214C10.0954 13.0595 10.507 13.0595 10.7609 12.8214C11.0147 12.5834 11.0147 12.1975 10.7609 11.9595L6.48882 7.95383C6.23496 7.71576 6.23496 7.32988 6.48882 7.09187L10.8096 3.04049C11.0635 2.80246 11.0635 2.41655 10.8096 2.17852Z" fill="currentColor"/>
          </svg>
        </template>
        <template #arrow-right>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M5.19038 2.17852C5.44428 1.94049 5.85582 1.94049 6.10972 2.17852L10.4288 6.22834C11.1902 6.94224 11.1904 8.09957 10.4294 8.81372L6.15841 12.8214C5.90457 13.0595 5.49297 13.0595 5.23913 12.8214C4.98529 12.5834 4.98529 12.1975 5.23913 11.9595L9.51118 7.95383C9.76504 7.71576 9.76504 7.32988 9.51118 7.09187L5.19038 3.04049C4.93654 2.80246 4.93654 2.41655 5.19038 2.17852Z" fill="currentColor"/>
          </svg>
        </template>
      </VueDatePicker>
    </div>
    <span class="input__label">{{ label }}</span>
  </div>
 
</template>

<style lang="scss">
.date-input {
  .dp__input {
    @include light-16;
    border: none;
    padding: 0;
    background: transparent;
  }

  .dp__menu {
    width: fit-content;
    min-width: auto;
    box-shadow: 0 1px 10px 0 rgba(0, 0, 0, 0.25);
    padding: size(18px) size(20px) size(48px) size(23px);
    border-radius: 15px;
  }

  .dp__menu_inner {
    padding: 0;
    margin-bottom: size(24px);
  }


  .dp__calendar_header_separator {
    display: none;
  }

  .dp__inner_nav {
    color: $light-grey;
    width: size(16px);
    height: size(16px);

    & svg {
      display: block;
      width: 100%;
      height: 100%;
    }
    
    @include hover {
      background: transparent;
      color: $blue-attention;
    }
  }

  .dp__calendar_header_item {
    @include small-bold;
    width: size(20px);
    height: size(20px);
    flex-grow: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .dp__cell_inner {
    @include small-bold;
    width: size(20px);
    height: size(20px);
    border-radius: 50%;
    flex-grow: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
  } 

  .dp__cell_disabled {
    color: $dark-grey;
  }
  
  .dp__calendar_item {
    flex-grow: 0;
  }

  .dp__calendar_row {
    gap: size(8px);
  }

  .dp__calendar_header {
    gap: size(8px);
  }

  .dp__month_year_wrap {
    order: -1;
  }

  .dp__arrow_top {
    display: none;
  }

  .dp--header-wrap {
    margin-bottom: size(16px)
  }

  .dp__month_year_select {
    @include small-bold;
    margin-right: auto;
    padding: 0;
    width: fit-content;
  }

  .dp__month_year_select:hover {
    background: transparent;
  }

  .dp__today,
  .dp--future {
    background: #dae2ff;
    color: $blue-attention;
    border: none;

    @include hover {
      color: #ffffff;
      background-color: $blue-attention;
    }
  }

  .dp__active_date{
    color: #ffffff;
    background-color: $blue-attention;
  } 
}
</style>


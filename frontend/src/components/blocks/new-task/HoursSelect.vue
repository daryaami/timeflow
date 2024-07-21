<script setup>
import { ref } from "vue";

// Open
const isDropdownOpen = ref(false);  

const handleClickOutside = (event) => {
  if (!event.target.closest('.hours-select')) {
    closeDropdown();
  }
}

const openDropdown = () => {
  isDropdownOpen.value = true;
  document.addEventListener('click', handleClickOutside);
}

const closeDropdown = () => {
  isDropdownOpen.value = false;
  document.removeEventListener('click', handleClickOutside);
}

const buttonClickHandler = (e) => {
  e.preventDefault();
  isDropdownOpen.value? closeDropdown(): openDropdown(); 
}


// 

const currentOption = ref();

const hours = [
  {
    name: 'Personal Hours',
  },
  {
    name: 'Working Hours',
  }
]

currentOption.value = hours[0];

const optionClickHandler = (option) => {
  currentOption.value = option;
  closeDropdown();
}
</script>

<template>
  <div class="hours-select input">
    <span class="input__input"
      @click="buttonClickHandler"
    >{{ currentOption.name }}</span>
    <span class="input__label">Hours</span>
    <div class="hours-select__arrow"
      :class="{'rotated': isDropdownOpen}"
    ></div>
    <ul v-if="isDropdownOpen"  class="hours-select__dropdown">
      <li class="hours-select__dropdown-item"
        v-for="(option, i) in hours"
        :key="i"
      >
        <div class="hours-select__dropdown-button"
          @click.stop="optionClickHandler(option)"
          tabindex="0"
        >
          <span>{{ option.name }}</span>
        </div>
      </li>
    </ul>
  </div>
</template>

<style lang="scss">
.hours-select {
  cursor: pointer;

  &__arrow {
    @include chevron-down;
    background-size: 100% 100%;
    position: absolute;
    right: size(16px);
    top: 50%;
    transform: translateY(-50%);
    width: size(20px);
    height: size(20px);
    transition: .2s;

    &.rotated {
      transform: translateY(-50%) rotate(-180deg);
    }
  }

  &__dropdown {
    @include reset-list;
    position: absolute;
    top: 100%;
    left: 0;
    padding-top: size(17px);
    padding-bottom: size(16px);
    background: $dark-white;
    border-radius: size(15px);
    width: 100%;
  }

  &__dropdown-item {
    @include light-16;

    & svg {
      display: block;
      width: size(17px);
      height: size(17px);
    }
  }

  &__dropdown-button {
    display: flex;
    align-items: center;
    gap: size(16px);
    padding: size(9px) size(21px) size(9px) size(21px);
    width: 100%;
    cursor: pointer;

    & span {
      white-space: nowrap;
    }

    @include hover {
      background: $dark-lines;
    }
  }
}
</style>
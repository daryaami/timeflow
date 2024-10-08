<script setup>
import { onMounted, ref, watch } from "vue";
import { useDropdown } from "@/components/composables/dropdown";
import { userData } from "@/components/js/data/userData";

const { isDropdownOpen, dropdownClickHandler, closeDropdown } = useDropdown();

const currentOption = ref();
const currentValue = defineModel();
const hours = ref(false);

const optionClickHandler = (option) => {
  currentOption.value = option;
  closeDropdown();
}

watch(currentOption, (newValue) => {
  currentValue.value = newValue.id;
})

onMounted(async () => {
  hours.value = userData.value.hours;
  currentOption.value = hours.value[0];
})
</script>

<template>
  <div class="hours-select input dropdown-wrapper">
    <div @click="dropdownClickHandler" class="input__input">
      <span v-if="currentOption">{{ currentOption.name }}</span>
      <div class="hours-select__arrow"
        :class="{'rotated': isDropdownOpen}"
      ></div>
    </div>
    <span class="input__label">Hours</span>
    <Transition name="dropdown">
      <ul v-if="isDropdownOpen && hours"  class="hours-select__dropdown">
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
    </Transition>
  </div>
</template>

<style lang="scss">
.hours-select {
  cursor: pointer;
  margin-bottom: size(30px);

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
    border-radius: size(15px);
    width: 100%;
    background: #ebf6ff;
    z-index: 100;
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
      background: #dee8f0;
    }
  }
}
</style>
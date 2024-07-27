<script setup>
import { onMounted, ref, watch } from "vue";
import { useDropdown } from "@/components/composables/dropdown";
import criticalPriorityIconVue from "../../icons/priorities/critical-priority-icon.vue";
import highPriorityIconVue from "../../icons/priorities/high-priority-icon.vue";
import mediumPriorityIconVue from "../../icons/priorities/medium-priority-icon.vue";
import lowPriorityIconVue from "../../icons/priorities/low-priority-icon.vue";

const { isDropdownOpen, dropdownClickHandler, closeDropdown } = useDropdown();

const currentOption = ref(null);
const currentValue = defineModel();

const priorities = [
  {
    icon: criticalPriorityIconVue,
    name: 'Critical',
    value: 'critical',
  },
  {
    icon: highPriorityIconVue,
    name: 'High priority',
    value: 'high',
  },
  {
    icon: mediumPriorityIconVue,
    name: 'Medium priority',
    value: 'medium',
  },
  {
    icon: lowPriorityIconVue,
    name: 'Low priority',
    value: 'low',
  },
]


currentOption.value = priorities[1];
currentValue.value = currentOption.value.value

const optionClickHandler = (option) => {
  currentOption.value = option;
  closeDropdown();
}

watch(currentOption, (newValue) => {
  currentValue.value = newValue.value;
})
</script>

<template>
  <div class="priority-select dropdown-wrapper">
    <button class="priority-select__button"
      @click="dropdownClickHandler"
    >
      <component :is="currentOption.icon"></component>
    </button>
    <Transition name="dropdown">
      <ul v-if="isDropdownOpen"  class="priority-select__dropdown">
        <li class="priority-select__dropdown-item"
          v-for="(option, i) in priorities"
          :key="i"
        >
          <div class="priority-select__dropdown-button"
            @click.stop="optionClickHandler(option)"
            tabindex="0"
          >
            <component :is="option.icon"></component>
            <span>{{ option.name }}</span>
          </div>
        </li>
      </ul>
    </Transition>
  </div>
</template>

<style lang="scss">
.priority-select {
  position: relative;
  z-index: 10;
  margin-left: size(29px);

  &__button {
    @include reset-button;
    width: size(42px);
    height: size(42px);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;

    & svg {
      display: block;
      width: size(30px);
      height: size(30px);
    }

    @include hover {
      background-color: $dark-white;
    }
  }

  &__dropdown {
    @include reset-list;
    position: absolute;
    top: 0;
    right: 0;
    padding-top: size(17px);
    padding-bottom: size(16px);
    background: #ebf6ff;
    border-radius: size(15px);
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
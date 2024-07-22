import { ref } from 'vue';

export function useDropdown() {
  const isDropdownOpen = ref(false);

  const handleClickOutside = (event) => {
    if (!event.target.closest('.dropdown-wrapper')) {
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

  const dropdownClickHandler= (e) => {
    e.preventDefault();
    isDropdownOpen.value ? closeDropdown() : openDropdown(); 
  }

  return { isDropdownOpen, handleClickOutside, openDropdown, closeDropdown, dropdownClickHandler };
}
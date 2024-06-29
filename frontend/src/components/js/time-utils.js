const getHours = (timeString) => {
  let date = new Date(timeString);
  return date.getHours()
}

const getMinutes = (timeString) => {
  let date = new Date(timeString);
  return date.getMinutes();
}

const getDecimalHours = (timeString) => {
  let date = new Date(timeString);
  let localHours = date.getHours();
  let minutes = date.getMinutes();
  return localHours + minutes / 60;
}

const getStringTime = (timeString) => {
  const date = new Date(timeString);
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  return `${hours}:${minutes}`;
};


export { getDecimalHours, getHours, getMinutes, getStringTime }
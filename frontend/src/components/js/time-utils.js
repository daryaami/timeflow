const getHours = (timeString) => {
  let date = new Date(timeString);
  return date.getHours()
}

const getMinutes = (timeString) => {
  let date = new Date(timeString);
  return date.getMinutes();
}

const getDecimalHours = (time) => {
  let date;

  if (typeof time === 'string') {
    date = new Date(time);
  } else {
    date = time
  }

  let localHours = date.getHours();
  let minutes = date.getMinutes();
  return localHours + minutes / 60;
}

const getStringTime = (time) => {
  let date;

  if (typeof time === 'string') {
    date = new Date(time);
  } else {
    date = time
  }

  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  return `${hours}:${minutes}`;
};

const getTomorrow = () => {
  const date = new Date();
  date.setDate(date.getDate() + 1);
  console.log(date)
  return date
}


export { getDecimalHours, getHours, getMinutes, getStringTime, getTomorrow }
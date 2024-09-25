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
  return date
}


const convertMinToTimeString = (value) => {
  const h = Math.floor(value / 60);
  const m = value % 60;

  if (h === 0) {
    return`${m} min`;
  } else if ((m === 0)) {
    return`${h} hr`;
  } else {
    return `${h} hr ${m} min`;
  }
}

const getStringDate = (dateString) => {
  const date = new Date(dateString);
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();

  return `${year}-${month}-${day}`;
}

const isSameDay = (date1, date2) => {
  return date1.getDate() === date2.getDate() &&
         date1.getMonth() === date2.getMonth() &&
         date1.getFullYear() === date2.getFullYear();
}

const getCurrentWeekMonday = (date) => {
  const currentDay = date.getDay(); 
  return new Date(date.setDate(date.getDate() - currentDay + 1));
}


export { getDecimalHours, getHours, getMinutes, getStringTime, getTomorrow, convertMinToTimeString, getStringDate, isSameDay, getCurrentWeekMonday }
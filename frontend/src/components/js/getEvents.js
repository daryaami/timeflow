const getEvents = async () => {
  let response = await fetch(`${window.location.origin}/planner_api/get_events/`);
  if (response.ok) {
    const data = await response.json();
    return data.days;
  } else {
    throw new Error('Failed to fetch events');
  }
}
export { getEvents }
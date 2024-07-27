const getUserData = async () => {
  let response = await fetch(`${window.location.origin}/user_api/get_user_info/`);
  if (response.ok) {
    const data = await response.json();
    return data;
  } else {
    throw new Error('Failed to fetch user data');
  }
}
export { getUserData }
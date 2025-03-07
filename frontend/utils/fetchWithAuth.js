async function fetchWithAuth(url, options = {}) {
  const token = localStorage.getItem("access_token");
  if (!token) {
    window.location.href = "/login";
    return;
  }
  options.headers = {
    ...(options.headers || {}),
    Authorization: `Bearer ${token}`,
  };
  return await fetch(`/${url}`, options);
}

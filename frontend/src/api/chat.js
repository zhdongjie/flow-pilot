export async function sendChat(message, currentPage) {
  const payload = {
    message,
    state: {},
  };

  if (currentPage) {
    payload.state.current_page = currentPage;
  }

  const response = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  return response.json();
}

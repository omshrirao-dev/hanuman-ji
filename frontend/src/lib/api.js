const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function sendChatMessage({ query, language = "auto", conversationId }) {
  const res = await fetch(`${API_BASE_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, language, conversation_id: conversationId }),
  });
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error(detail.detail || `Request failed (${res.status})`);
  }
  return res.json();
}

export async function fetchSources() {
  const res = await fetch(`${API_BASE_URL}/api/sources`);
  if (!res.ok) throw new Error("Failed to load sources");
  return res.json();
}

export async function sendFeedback({ messageId, rating, comment }) {
  const res = await fetch(`${API_BASE_URL}/api/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message_id: messageId, rating, comment }),
  });
  if (!res.ok) throw new Error("Failed to send feedback");
  return res.json();
}

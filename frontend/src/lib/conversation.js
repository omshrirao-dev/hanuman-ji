const STORAGE_KEY = "hanuman-ji-conversation";

export function loadConversation() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

export function saveConversation(messages) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
}

export function clearConversation() {
  localStorage.removeItem(STORAGE_KEY);
}

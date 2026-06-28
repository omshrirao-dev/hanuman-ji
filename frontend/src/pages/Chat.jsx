import { useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import MessageBubble from "../components/MessageBubble";
import VoiceButton from "../components/VoiceButton";
import { useSpeechRecognition } from "../hooks/useSpeechRecognition";
import { useSpeechSynthesis } from "../hooks/useSpeechSynthesis";
import { sendChatMessage } from "../lib/api";
import { loadConversation, saveConversation } from "../lib/conversation";

export default function Chat() {
  const navigate = useNavigate();
  const location = useLocation();
  const [messages, setMessages] = useState(() => loadConversation());
  const [input, setInput] = useState(location.state?.prefill || "");
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState(null);
  const [speakingId, setSpeakingId] = useState(null);
  const bottomRef = useRef(null);

  const { speak, stop, isSupported: ttsSupported } = useSpeechSynthesis();
  const { isListening, isSupported: sttSupported, start, stop: stopListening } = useSpeechRecognition({
    lang: "hi-IN",
    onResult: (text) => setInput(text),
  });

  useEffect(() => {
    saveConversation(messages);
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend(e) {
    e.preventDefault();
    const query = input.trim();
    if (!query || isSending) return;

    const userMessage = { id: crypto.randomUUID(), role: "user", text: query };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setError(null);
    setIsSending(true);

    try {
      const result = await sendChatMessage({ query, conversationId: "local" });
      const guideMessage = {
        id: crypto.randomUUID(),
        role: "guide",
        text: result.response,
        sources: result.sources,
        language: result.language,
      };
      setMessages((prev) => [...prev, guideMessage]);
      speak(result.response, result.language);
      setSpeakingId(guideMessage.id);
    } catch (err) {
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setIsSending(false);
    }
  }

  function handlePlayAudio(message) {
    if (speakingId === message.id) {
      stop();
      setSpeakingId(null);
    } else {
      speak(message.text, message.language);
      setSpeakingId(message.id);
    }
  }

  function handleMicClick() {
    if (isListening) stopListening();
    else start();
  }

  return (
    <div className="flex h-screen flex-col">
      <header className="flex items-center justify-between border-b border-muted/20 px-4 py-3">
        <button onClick={() => navigate("/")} className="font-devanagari text-lg text-saffron">
          हनुमान जी
        </button>
        <button onClick={() => navigate("/about")} className="text-sm text-muted hover:text-saffron">
          About
        </button>
      </header>

      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="mx-auto flex max-w-2xl flex-col gap-4">
          {messages.length === 0 && (
            <p className="text-center text-sm text-muted">
              अपनी बात कहें... Share what's on your mind, in Hindi, English, or Hinglish.
            </p>
          )}
          {messages.map((m) => (
            <MessageBubble
              key={m.id}
              message={m}
              onPlayAudio={handlePlayAudio}
              isSpeaking={speakingId === m.id}
            />
          ))}
          {isSending && <p className="text-sm text-muted">हनुमान जी सोच रहे हैं...</p>}
          {error && <p className="text-sm text-rose">{error}</p>}
          <div ref={bottomRef} />
        </div>
      </div>

      <form onSubmit={handleSend} className="border-t border-muted/20 px-4 py-3">
        <div className="mx-auto flex max-w-2xl items-center gap-2">
          <VoiceButton isListening={isListening} isSupported={sttSupported} onClick={handleMicClick} />
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="अपनी बात कहें... / Share what's on your mind..."
            className="font-devanagari flex-1 rounded-full bg-card px-4 py-3 text-warmwhite placeholder-muted outline-none focus:ring-1 focus:ring-saffron"
          />
          <button
            type="submit"
            disabled={isSending || !input.trim()}
            className="shrink-0 rounded-full bg-gradient-to-r from-saffron to-rose px-5 py-3 text-sm font-medium text-bg disabled:opacity-40"
          >
            📤
          </button>
        </div>
      </form>
    </div>
  );
}

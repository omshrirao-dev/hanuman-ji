export default function VoiceButton({ isListening, isSupported, onClick }) {
  if (!isSupported) return null;

  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={isListening ? "Stop listening" : "Start voice input"}
      className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-full text-lg transition ${
        isListening
          ? "animate-pulse-ring bg-saffron text-bg"
          : "bg-card text-muted hover:text-saffron"
      }`}
    >
      🎤
    </button>
  );
}

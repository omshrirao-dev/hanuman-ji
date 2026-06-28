export default function MessageBubble({ message, onPlayAudio, isSpeaking }) {
  const isUser = message.role === "user";

  if (isUser) {
    return (
      <div className="flex justify-end">
        <div className="font-devanagari max-w-[80%] rounded-2xl bg-card px-4 py-3 text-warmwhite">
          {message.text}
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-start">
      <div className="font-devanagari max-w-[80%] rounded-2xl border-l-4 border-saffron bg-card px-4 py-3 text-warmwhite">
        <p className="whitespace-pre-wrap">{message.text}</p>

        {message.sources?.length > 0 && (
          <div className="mt-3 space-y-1 border-t border-muted/20 pt-2 text-xs text-muted">
            {message.sources.map((s) => (
              <p key={s.id}>
                📖 {s.source?.split(",")[0] || s.type} — {s.title}
              </p>
            ))}
          </div>
        )}

        <button
          onClick={() => onPlayAudio?.(message)}
          className="mt-2 flex items-center gap-1 text-xs text-saffron hover:text-rose"
        >
          {isSpeaking ? "⏸ pause" : "🔊 play"}
        </button>
      </div>
    </div>
  );
}

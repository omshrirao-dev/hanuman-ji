import { useNavigate } from "react-router-dom";

export default function About() {
  const navigate = useNavigate();

  return (
    <div className="mx-auto max-w-2xl px-6 py-12 text-warmwhite">
      <button onClick={() => navigate("/")} className="font-devanagari text-saffron">
        ← हनुमान जी
      </button>

      <h1 className="font-devanagari mt-6 text-3xl font-semibold">हनुमान जी क्या है?</h1>
      <p className="mt-2 text-muted">What is Hanuman Ji?</p>

      <p className="mt-6 leading-relaxed text-warmwhite/90">
        Hanuman Ji is an AI spiritual companion that listens to the real problems
        people face — career stress, money worries, family conflict, relationship
        pain, mental anxiety — and responds with relevant wisdom from the Shiv
        Mahapuran and the Bhagavad Gita, in Hindi, English, or Hinglish, with voice.
      </p>

      <h2 className="mt-8 text-xl font-semibold">Sources</h2>
      <ul className="mt-2 list-inside list-disc text-warmwhite/80">
        <li>Shiv Mahapuran Katha — Pandit Pradeep Ji Mishra (Sehore Wale), Bathinda 2026 — 28 teachings + 5 upays</li>
        <li>Bhagavad Gita — all 18 chapters, 700+ shlokas</li>
      </ul>

      <h2 className="mt-8 text-xl font-semibold">How it works</h2>
      <p className="mt-2 leading-relaxed text-warmwhite/80">
        Your message is matched by meaning, not keywords, to the most relevant
        teaching or shloka, then woven into a warm, grounded response — never
        invented, always cited.
      </p>

      <p className="mt-8 rounded-xl border border-muted/20 bg-card p-4 text-sm text-muted">
        Hanuman Ji is an AI guide. For serious health, legal, or mental health
        concerns, please consult a qualified professional. Conversations are
        stored only in your browser and are never sent anywhere except as the
        current question to generate a response.
      </p>
    </div>
  );
}

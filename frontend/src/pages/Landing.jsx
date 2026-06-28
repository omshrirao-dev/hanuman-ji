import { useNavigate } from "react-router-dom";

const SAMPLE_QUESTIONS = [
  "मुझे नौकरी नहीं मिल रही 😔",
  "घर में शांति नहीं है",
  "I'm stressed about money",
  "Relationship mein problems hain",
];

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="flex min-h-screen flex-col items-center justify-center px-6 py-16 text-center">
      <p className="font-devanagari text-sm uppercase tracking-widest text-saffron">
        ॐ श्री हनुमते नमः
      </p>
      <h1 className="font-devanagari mt-4 text-5xl font-semibold text-warmwhite sm:text-6xl">
        हनुमान जी
      </h1>
      <p className="mt-1 text-xl text-muted">Hanuman Ji</p>

      <p className="font-devanagari mt-8 max-w-xl text-lg text-warmwhite/90">
        जीवन की हर उलझन का उत्तर — शिव महापुराण और भगवद्गीता की वाणी में
      </p>
      <p className="mt-2 max-w-xl text-base text-muted">
        Every life problem has an answer — in the wisdom of Shiv Mahapuran and
        Bhagavad Gita.
      </p>

      <button
        onClick={() => navigate("/chat")}
        className="mt-10 rounded-full bg-gradient-to-r from-saffron to-rose px-8 py-3 text-base font-medium text-bg shadow-lg transition hover:opacity-90"
      >
        Start Conversation
      </button>

      <div className="mt-12 flex max-w-2xl flex-wrap items-center justify-center gap-3">
        {SAMPLE_QUESTIONS.map((q) => (
          <button
            key={q}
            onClick={() => navigate("/chat", { state: { prefill: q } })}
            className="font-devanagari rounded-full border border-muted/30 bg-card px-4 py-2 text-sm text-warmwhite/80 transition hover:border-saffron/60 hover:text-saffron"
          >
            {q}
          </button>
        ))}
      </div>

      <nav className="mt-16 flex gap-6 text-sm text-muted">
        <button onClick={() => navigate("/about")} className="hover:text-saffron">
          About
        </button>
      </nav>
    </div>
  );
}

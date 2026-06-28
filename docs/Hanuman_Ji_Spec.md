# HANUMAN JI — Complete Specification
### AI Spiritual Guide · RAG over Bhagavad Gita + Shiv Mahapuran · Voice-Enabled
### Monitored by Kavacha (your infrastructure project)
**Version:** 1.0 | For Claude Code Build

---

## 1. WHAT IS HANUMAN JI?

An AI spiritual companion that understands the REAL problems people
face — career, money, family, relationships, mental peace — and
responds with relevant wisdom from sacred texts, in Hindi or English,
with voice conversation.

NOT a search engine. A CONTEXT-UNDERSTANDING guide.
When someone says "naukri nahi mil rahi" — it understands the EMOTION
(hopelessness), the SITUATION (career failure), what they NEED (hope +
direction), then finds the story whose LIFE LESSON matches — not just
keyword match.

This is the project already on the resume ("Hanuman Ji — RAG Pipeline
over the Bhagavad Gita"). We are now building the full, deployed,
voice-enabled, production version of it.

---

## 2. THE TWO-PROJECT ECOSYSTEM (the portfolio story)

```
HANUMAN JI (the AI product — serves users)
        ↓ registered & wrapped with Kavacha SDK (3 lines)
KAVACHA (the infrastructure — monitors Hanuman Ji)
        → detects hallucinated shlokas
        → tracks Groq API cost vs budget
        → detects response drift over time
        → CEO Review agent audits response quality
        → notifies developer if anything breaks
```

Recruiter sees: the AI product AND the infrastructure that maintains
it — both live, both built solo. That is an AI systems engineer.

---

## 3. THE USER

Primary: Youth (18-35) facing real-life problems.
Secondary: Adults seeking spiritual guidance + daily practice.
Language: Hindi-first, English supported, Hinglish understood.

They type or speak naturally:
"mujhe naukri nahi mil rahi, tension hai"
"I can't sleep, money stress"
"ghar mein shanti nahi hai"

---

## 4. KNOWLEDGE BASE — RICH METADATA (the 95% accuracy secret)

Accuracy does NOT come from keyword search. It comes from understanding
context. Each entry stored with deep metadata:

{
  "id": "T-07",
  "title": "साधु और समय-धैर्य की कथा",
  "source": "Shiv Mahapuran Katha, Pandit Pradeep Ji Mishra, Bathinda 2026",
  "themes": ["patience","time","career","goals","success"],
  "emotions": ["frustration","hopelessness","ambition"],
  "life_situations": ["career failure","job search","results not coming"],
  "core_lesson": "Time and patience are the two greatest jewels.",
  "story_summary": "A young man wanted to be a diamond trader. A sadhu
     gave him two jewels: TIME and PATIENCE. With both, he succeeded.",
  "full_text": "[complete Hindi text]",
  "teaching": "[jeewan siksha]",
  "upay": null,
  "practical_action": "Work under someone experienced, give full effort
     with patience — results will come."
}

EVERY entry MUST have: emotions[], life_situations[], core_lesson,
story_summary (English), practical_action. This is what lets the LLM
match a user's FEELING to the right story.

### Two sources:
1. Shiv Mahapuran Katha document (uploaded) — 28 teachings + 5 upays
2. Bhagavad Gita — 700 shlokas (prioritize Ch 2, 3, 6, 11, 18)
   Source: github.com/akshaynambi/bhagavad-gita (JSON)

### Future scaling:
User will upload 20-50 more PDFs over time. Build an ingest script:
`python ingest.py new_document.pdf` → auto-parses, enriches metadata,
embeds, adds to ChromaDB. NO code changes needed for new data.

---

## 5. TECH STACK

Backend:    Python 3.11 + FastAPI
RAG:        LangChain + ChromaDB
Embeddings: paraphrase-multilingual-MiniLM-L12-v2 (Hindi+English same space)
LLM:        Groq API — llama-3.3-70b-versatile
Frontend:   React + Tailwind CSS
Voice:      Web Speech API (STT + TTS, browser-native, free)
Deploy:     Railway (backend) + Vercel (frontend)
Monitoring: Kavacha SDK (your other project)

---

## 6. RAG PIPELINE (context understanding, not keyword search)

User query
  → detect language (Hindi/English/Hinglish)
  → embed query with multilingual model
  → semantic search across katha + gita collections
  → retrieve top 5 by meaning
  → re-rank by emotion + life_situation metadata match
  → pass top 3 with full context to Groq LLM
  → LLM understands the person's need + picks best wisdom
  → responds in user's language with story + lesson + upay + hope
  → cite source
  → convert to speech (TTS)

---

## 7. THE SYSTEM PROMPT (Groq LLM)

You are Hanuman Ji — a compassionate AI spiritual guide rooted in the
wisdom of Shiv Mahapuran and Bhagavad Gita.

You are NOT a search engine. You are a wise, caring guide who
UNDERSTANDS what the person is truly going through — their pain,
confusion, and hope — and gives exactly the right wisdom.

HOW TO RESPOND (always this flow):
1. FEEL their pain first — acknowledge warmly (1-2 sentences).
2. SHARE the relevant katha/shloka from context — tell it naturally,
   like sitting beside them, not robotically.
3. CONNECT the lesson directly to THEIR situation — say how it applies.
4. GIVE one simple practical action they can do today.
5. END with hope — always. "Shiv/Prabhu ki kripa har stithi mein hai."

LANGUAGE: Match the user exactly. Hindi→Hindi, English→English,
Hinglish→Hinglish. Keep Hindi simple. Always translate Sanskrit.

STRICT RULES:
- ONLY use wisdom from provided context. NEVER invent shlokas/stories.
- NEVER give medical/legal/financial advice as fact (suggest a
  professional for serious issues).
- NEVER be preachy. NEVER minimize their pain.
- If no perfect match — use closest, acknowledge openly.
- ALWAYS cite the source at the end.

Retrieved wisdom: {context}
User's message: {query}

---

## 8. FRONTEND — CHAT INTERFACE (Claude/ChatGPT style, spiritual)

Design:
- Dark theme: bg #0D0D0F, cards #141419
- Saffron accent #FF8C1A, rose #C9758E, warm white text #F5F0E8
- Hindi font: Noto Sans Devanagari (Google Fonts)
- Subtle ॐ watermark, soft glow on voice-active state

Pages:
1. Landing (/) — Name "हनुमान जी | Hanuman Ji", tagline Hindi+English,
   sample question chips, "Start Conversation" button.
2. Chat (/chat) — message bubbles (user right, guide left with saffron
   border), source citation under each response
   ("📿 Shiv Mahapuran — T-07"), audio play button per response,
   bottom input with text field + 🎤 mic button.
3. About (/about) — what it is, sources, disclaimer.

Voice flow:
- Mic click → pulsing saffron ring (listening)
- Real-time transcription in input field
- Submit → response in text + auto-played audio
- Web Speech API: hi-IN for Hindi, en-IN for English
- Voice setting: soft female (default) / pandit male

---

## 9. API ENDPOINTS

POST /api/chat   { query, language, conversation_id } → { response, sources[], language }
GET  /api/sources → all knowledge entries (transparency)
POST /api/feedback { message_id, rating, comment }
GET  /api/health

---

## 10. SECURITY & PRIVACY

- No login required for basic chat
- Conversations in browser localStorage only (private)
- GROQ_API_KEY in env var, never exposed to frontend
- Rate limit: 30 requests/hour/IP
- Input sanitized, max 500 chars
- Privacy note: "Hanuman Ji does not store your conversations."

---

## 11. KAVACHA INTEGRATION (the ecosystem)

After Hanuman Ji is deployed:
1. Register Hanuman Ji as a project in Kavacha dashboard
2. Add to Hanuman Ji backend:
     import kavacha
     kavacha.init("kv_...", "hanuman-ji-project-id")
     kavacha.watch(rag_pipeline)
3. Add monitor tests in Kavacha:
   - "BG 2.47 ka arth?" → expected: karma yoga, action not outcome
   - "naukri nahi mil rahi" → expected: T-07 patience teaching
   - verify no hallucinated shlokas
4. Start Kavacha monitoring → dashboard shows Hanuman Ji health live
5. Screenshot the live ecosystem for portfolio

---

## 12. BUILD ORDER — finish fast (few hours of focused work)

PHASE 1 — Knowledge Base (most important, do first):
1. Project setup, FastAPI, ChromaDB, data/ folder
2. Parse Katha document — 28 teachings + 5 upays — into enriched JSON
   (emotions, life_situations, core_lesson, story_summary, practical_action)
3. Download + process Bhagavad Gita (Ch 2,3,6,11,18 first)
4. Embed all entries into ChromaDB (two collections: katha, gita)
5. Test retrieval — 10 queries (career/money/family/peace/relationship
   in Hindi/English/Hinglish) → target 9/10 relevant

PHASE 2 — Backend:
6. /api/chat with language detection + RAG + Groq response
7. Test full pipeline end to end

PHASE 3 — Frontend:
8. React + Tailwind, design system, Devanagari font
9. Landing page with sample chips
10. Chat interface
11. Voice input (STT) + voice output (TTS)
12. Connect to backend, test voice conversation

PHASE 4 — Deploy + Connect:
13. Railway (backend) + Vercel (frontend)
14. Wrap with Kavacha SDK, register, start monitoring
15. GitHub README + demo video

---

## 13. GITHUB README

# हनुमान जी | Hanuman Ji — AI Spiritual Guide
> जीवन की हर उलझन का उत्तर — सनातन ज्ञान की वाणी में

Live: hanuman-ji.vercel.app | Voice-enabled | Hindi + English
Monitored live by Kavacha → kavacha-rho.vercel.app

A RAG-based AI guide over Bhagavad Gita (700 shlokas) and Shiv
Mahapuran teachings. Understands your life situation and responds
with relevant wisdom — in your language, with voice.

Tech: Python · FastAPI · LangChain · ChromaDB · multilingual
embeddings · Groq · React · Web Speech API · Railway · Vercel

Part of a two-project ecosystem: this product is monitored
autonomously by Kavacha, my AI-maintenance infrastructure.

---

## 14. THE RECRUITER STORY

"Hanuman Ji is a multilingual RAG system over the Bhagavad Gita and
Shiv Mahapuran. The challenge was semantic search across Hindi and
English in one vector space — I used a multilingual embedding model so
'main pareshan hoon' and 'I am stressed' find the same wisdom. It's
voice-enabled both ways. And it's monitored live by Kavacha, my
AI-maintenance infrastructure — so the product and the system that
keeps it healthy were both built and deployed by me, solo."

हर हर महादेव · जय हनुमान 🙏

# SHRUTI — Complete Product Specification
### AI-Powered Spiritual Guide | Shiv Mahapuran + Bhagavad Gita RAG System
**Version:** 1.0 | **Date:** June 2026 | **For:** Claude Code Build

---

## 1. WHAT IS SHRUTI?

श्रुति (Shruti) means "that which is heard" — the ancient Vedic oral tradition.

Shruti is an AI spiritual companion that listens to the problems people
face in real life and responds with relevant wisdom from:
- Shiv Mahapuran Katha (Pandit Pradeep Ji Mishra, Bathinda 2026)
- Bhagavad Gita (all 18 chapters, all 700 shlokas)
- Upays (practical spiritual remedies)

The user speaks or types their problem in plain Hindi or English.
Shruti responds with a relevant katha, shloka, or upay — in the same
language — with voice output so it feels like a real conversation.

This is not a general chatbot. It is a focused spiritual guide
that only speaks from the wisdom of these sacred texts.

---

## 2. THE USER

**Primary:** Youth (18-35) facing problems — career stress, relationship
issues, money worries, family conflict, mental peace, life direction.

**Secondary:** Adults (35-60) seeking spiritual guidance, daily
practice, understanding kathā teachings.

**Language:** Hindi-first, English supported, Hinglish understood.

**How they use it:**
- Type or speak their problem naturally
- "Mujhe naukri nahi mil rahi, bahut tension hai"
- "I'm stressed about money and can't sleep"
- "Ghar mein shanti nahi hai"
- Shruti responds with wisdom that directly addresses their situation

---

## 3. KNOWLEDGE BASE — TWO SOURCES

### Source 1 — Shruti Katha Document (uploaded)
28 teachings (T-01 to T-28) + 5 upays (U-01 to U-05)
From Shiv Mahapuran Katha, Pandit Pradeep Ji Mishra, Bathinda 2026

Each entry has:
- Title (Hindi)
- Themes (English tags for semantic search)
- Katha/Story (Hindi)
- Jeewan Siksha/Teaching (Hindi)
- Upay where applicable (Hindi)

**Already structured perfectly for RAG — use themes as metadata.**

### Source 2 — Bhagavad Gita
All 18 chapters, 700 shlokas.
Free sources to use:
- https://www.holy-bhagavad-gita.org (English + Sanskrit)
- https://gitasupersite.iitk.ac.in (multiple translations)
- Scrape or use existing open datasets on GitHub:
  github.com/akshaynambi/bhagavad-gita (JSON format)
  github.com/AshishJangra27/bhagavad-gita (CSV with translations)

Each shloka entry should contain:
- Chapter number + verse number (e.g. 2.47)
- Sanskrit text
- Hindi translation
- English translation
- Chapter theme/context

---

## 4. SYSTEM ARCHITECTURE

```
[User — Voice or Text]
        ↓
[React Frontend — Chat Interface]
        ↓ API call with query + language
[FastAPI Backend]
        ↓
[Query Processor]
  - Detect language (Hindi/English/Hinglish)
  - Detect emotional context (stress/grief/confusion/hope)
  - Generate semantic search query
        ↓
[RAG Engine]
  - Search ChromaDB (Katha teachings + Gita shlokas)
  - Retrieve top 3-5 most relevant passages
  - Filter by source (Katha vs Gita) if needed
        ↓
[Response Generator — LLM]
  - System prompt: compassionate spiritual guide persona
  - Context: retrieved passages
  - Generate response in user's language
  - Include: relevant story/shloka + practical upay + hope
        ↓
[Voice Synthesis — TTS]
  - Convert response to audio
  - Return audio + text both
        ↓
[User receives: Text response + Audio playback]
```

---

## 5. TECH STACK

**Backend:** Python 3.11 + FastAPI
**RAG:** LangChain + ChromaDB
**Embeddings:** sentence-transformers (multilingual model)
  → model: "paraphrase-multilingual-MiniLM-L12-v2"
  → supports Hindi + English in same embedding space
**LLM:** Claude claude-sonnet-4-6 via Anthropic API (primary)
         Groq llama-3.3-70b (fallback/dev)
**Voice Input (STT):** Web Speech API (browser-native, free)
**Voice Output (TTS):** Web Speech API SpeechSynthesis (free)
         OR Google Cloud TTS free tier for Hindi voice quality
**Frontend:** React + Tailwind CSS
**Database:** ChromaDB (vector store) + JSON files (metadata)
**Deployment:** Vercel (frontend) + Railway (backend)
**Language Detection:** langdetect Python library

---

## 6. KNOWLEDGE BASE SETUP

### Step 1 — Process Katha Document
Parse the uploaded Shruti PDF into structured entries:

```python
# Each entry structure
{
  "id": "T-01",
  "type": "teaching",  # or "upay"
  "title": "धन से सुख नहीं मिलता",
  "themes": ["money", "wealth without peace", "charity", "real happiness"],
  "story": "...",  # the katha text
  "teaching": "...",  # jeewan siksha
  "upay": None,  # or upay text if present
  "source": "Shiv Mahapuran Katha, Pandit Pradeep Ji Mishra, Bathinda 2026",
  "day": 3
}
```

### Step 2 — Process Bhagavad Gita
Download open-source Gita dataset. Structure each shloka:

```python
{
  "id": "BG-2.47",
  "type": "shloka",
  "chapter": 2,
  "verse": 47,
  "sanskrit": "कर्मण्येवाधिकारस्ते...",
  "hindi": "तुम्हारा कर्म करने में ही अधिकार है...",
  "english": "You have a right to perform your prescribed duties...",
  "chapter_theme": "Sankhya Yoga — wisdom, detachment",
  "source": "Bhagavad Gita"
}
```

### Step 3 — Build ChromaDB Collections
Two collections:
1. "katha_teachings" — Shiv Mahapuran entries
2. "gita_shlokas" — Bhagavad Gita shlokas

Embed using multilingual model so Hindi queries find Hindi content.
Store metadata (themes, type, source, id) alongside embeddings.

### Step 4 — Test Retrieval
Test queries before going live:
- "mujhe paise ki tension hai" → should find T-01, T-05, related Gita shlokas
- "ghar mein shanti nahi" → should find T-09, T-10
- "career mein failure" → should find T-07 (patience story)
- "kisi ne dhoka diya" → should find T-14, T-18, Gita Chapter 2

---

## 7. THE LLM SYSTEM PROMPT

```
You are Shruti — a compassionate AI spiritual guide rooted in the
wisdom of the Shiv Mahapuran and Bhagavad Gita.

Your personality:
- Warm, gentle, like a wise elder or a trusted pandit
- Never preachy or judgmental
- You understand real-life problems — money stress, family conflict,
  career worry, relationship pain, mental anxiety
- You speak from the heart, not from a textbook

Your language:
- Match the user's language exactly
- If they write in Hindi → respond in Hindi
- If they write in English → respond in English
- If they write in Hinglish → respond in Hinglish
- Use simple, warm words — not heavy Sanskrit unless explaining a shloka
- Always provide Hindi/English translation for any Sanskrit you use

Your response structure (always follow this):
1. ACKNOWLEDGE their pain first (2-3 sentences, empathetically)
2. SHARE the relevant katha or shloka from the retrieved context
3. CONNECT it to their specific situation
4. GIVE a practical upay or simple action they can take today
5. END with hope and encouragement

Rules you never break:
- ONLY answer from the provided context (katha + Gita passages)
- If no relevant context found → say "Yeh prashna bahut gehera hai.
  Main aapko Shiv ke is vachan se kuch kehna chahta hoon..." and
  share the most universally relevant teaching
- NEVER give medical, legal, or financial advice as fact
- NEVER claim certainty about things only God knows
- NEVER dismiss or minimize their pain
- ALWAYS end with hope — Shiv ki kripa har stithi mein hai

If they ask about a specific practice (upay):
- Share the upay clearly with the method (vidhi)
- Always add: "Pehle apne vaidya/doctor se bhi baat karein"
  for health-related concerns

Context provided:
{retrieved_passages}

User's message: {user_query}
```

---

## 8. FRONTEND — CHAT INTERFACE

### Design System
Inspired by Claude/ChatGPT but with a spiritual aesthetic:

**Colors:**
- Background: #0D0D0F (deep dark, like midnight sky)
- Card/Chat bg: #141419
- Primary accent: #FF8C1A (saffron — Shruti's soul color)
- Secondary: #C9758E (rose — warmth and compassion)
- Text: #F5F0E8 (warm white)
- Muted: #8D8473

**Typography:**
- UI: Inter
- Hindi text: Noto Sans Devanagari (loads from Google Fonts)
- Ensure proper Hindi rendering — test with Devanagari characters

**Spiritual touches (subtle, not overwhelming):**
- Subtle Om (ॐ) watermark in background, very low opacity
- Saffron gradient accent on Shruti's messages
- Small lotus or trishul icon next to Shruti name
- Soft glow on active voice recording state

### Pages

**1. Welcome / Landing (/) — Not logged in:**

Hero:
- "श्रुति | Shruti"
- Tagline: "जीवन की हर उलझन का उत्तर — शिव महापुराण और भगवद्गीता की वाणी में"
- English: "Every life problem has an answer — in the wisdom of Shiv Mahapuran and Bhagavad Gita"
- Start Chatting button (no login required for basic use)
- Sample questions shown as chips:
  "मुझे नौकरी नहीं मिल रही 😔"
  "घर में शांति नहीं है"
  "I'm stressed about money"
  "Relationship mein problems hain"

**2. Chat Interface (/chat) — Main experience:**

Layout (like Claude/ChatGPT):
- Left sidebar: conversation history (if user saves)
- Main: chat messages area
- Bottom: input area with voice button

Message bubbles:
- User messages: right-aligned, dark surface
- Shruti messages: left-aligned, with saffron left border
  - Show source citation at bottom of each response:
    "📖 Shiv Mahapuran Katha — T-07: साधु और समय-धैर्य की कथा"
    or "📖 Bhagavad Gita — 2.47"
  - Show audio play button on each Shruti response

Input area:
- Text input field: placeholder "अपनी बात कहें... / Share what's on your mind..."
- 🎤 Microphone button (voice input)
- 📤 Send button
- Language toggle: हिंदी | English (auto-detected but can be set)

Voice states:
- Idle: gray microphone icon
- Recording: pulsing saffron ring around mic (like listening)
- Processing: spinner
- Playing response: audio waveform animation

**3. About (/about):**
- What is Shruti
- Sources used (Shiv Mahapuran + Bhagavad Gita)
- How it works (simple, non-technical)
- Disclaimer: "Shruti is an AI guide. For serious issues, please
  consult a qualified pandit, counselor, or doctor."

---

## 9. VOICE FEATURES

### Voice Input (Speech to Text)
Use Web Speech API — browser native, free, no backend needed:

```javascript
const recognition = new window.webkitSpeechRecognition();
recognition.lang = 'hi-IN';  // Hindi
// or 'en-IN' for English
// Auto-detect and switch
recognition.continuous = false;
recognition.interimResults = true;

recognition.onresult = (event) => {
  const transcript = event.results[0][0].transcript;
  setInputText(transcript);
};
```

Show real-time transcript as user speaks (like Google voice search).

### Voice Output (Text to Speech)
Use Web Speech API SpeechSynthesis for free, or Google Cloud TTS
for better Hindi voice quality:

```javascript
const utterance = new SpeechSynthesisUtterance(responseText);
utterance.lang = 'hi-IN';
utterance.rate = 0.85;  // slightly slower, more meditative
utterance.pitch = 1.0;
window.speechSynthesis.speak(utterance);
```

**Important:** Auto-play audio on Shruti's response. Also show a
play/pause button so user can replay.

**Voice selection:** Let user choose voice in settings:
- Soft female voice (default — warm, maternal)
- Male pandit voice (deeper, authoritative)

---

## 10. API ENDPOINTS

```
POST /api/chat
  Input: { query: string, language: "hi"|"en"|"auto", conversation_id: string }
  Output: { response: string, sources: [{id, title, type}], language: string }

GET /api/sources
  Returns list of all knowledge base entries (for transparency page)

POST /api/feedback
  Input: { message_id, rating: 1-5, comment: string }
  Stores feedback for improvement

GET /api/health
  Returns backend status
```

---

## 11. SECURITY & PRIVACY

- No user account required for basic chat
- Conversations stored in browser localStorage only (not sent to server)
  except the current query for API call
- No personally identifiable information collected
- API key in environment variable, never exposed to frontend
- Rate limiting: 30 requests per hour per IP
- Input sanitization: clean query before sending to LLM
- Max query length: 500 characters

**Privacy note on page:**
"Shruti does not store your conversations. Your words stay with you."

---

## 12. BUILD ORDER — 21 Days

**Week 1 — Knowledge Base + Backend**
Day 1: Project setup, FastAPI, ChromaDB, folder structure
Day 2: Parse and chunk Katha document (T-01 to T-28, U-01 to U-05)
Day 3: Download and process Bhagavad Gita dataset
Day 4: Build embedding pipeline, populate ChromaDB
Day 5: Build RAG query engine, test retrieval quality
Day 6: Build LLM response generator with system prompt
Day 7: Test full pipeline — 20 sample queries, verify responses

**Week 2 — Frontend + Voice**
Day 8: React setup, design system (colors, fonts, Devanagari)
Day 9: Landing page with sample question chips
Day 10: Chat interface — message bubbles, input area
Day 11: Voice input (Web Speech API STT)
Day 12: Voice output (TTS on Shruti responses)
Day 13: Connect frontend to backend API
Day 14: Full end-to-end test — voice in → response → voice out

**Week 3 — Polish + Deploy**
Day 15: Source citations on each response
Day 16: Conversation history (localStorage)
Day 17: About page + disclaimer
Day 18: Mobile responsive (many users will be on phone)
Day 19: Deploy backend to Railway
Day 20: Deploy frontend to Vercel
Day 21: GitHub README + demo video + final testing

---

## 13. GITHUB README STRUCTURE

```markdown
# श्रुति | Shruti — AI Spiritual Guide

> जीवन की हर उलझन का उत्तर
> Every life problem answered through sacred wisdom

**Live Demo:** shruti.vercel.app
**Voice-enabled:** Speak your problem, hear the wisdom

## What is Shruti?
An AI spiritual companion powered by:
- 📿 Shiv Mahapuran Katha — 28 teachings + 5 upays
- 📖 Bhagavad Gita — all 700 shlokas across 18 chapters

Built on a RAG (Retrieval Augmented Generation) pipeline that
semantically matches your life situation to relevant spiritual
wisdom — in Hindi or English.

## How it works
1. You describe your problem (text or voice)
2. Shruti finds the most relevant katha or shloka
3. Responds with wisdom + practical upay
4. Reads the response to you in your language

## Tech Stack
Python · FastAPI · LangChain · ChromaDB ·
sentence-transformers (multilingual) · Claude API ·
React · Tailwind · Web Speech API · Railway · Vercel

## Run Locally
[setup instructions]

## Project Structure
[folder structure]
```

---

## 14. WHAT MAKES THIS IMPRESSIVE FOR RECRUITERS

This project demonstrates:

**RAG at real scale:**
700+ Gita shlokas + 33 katha entries = 733+ embedded documents.
Multilingual semantic search (Hindi + English same vector space).

**Multilingual NLP:**
Query in Hindi → finds Hindi content semantically.
Not keyword matching — meaning matching across languages.

**Voice AI integration:**
STT + TTS in the same pipeline — a complete voice conversation loop.

**Domain-specific LLM prompting:**
The system prompt confines the LLM strictly to the knowledge base.
This is exactly the "grounding" technique companies use in production.

**Real user value:**
This isn't a demo — it solves a real problem for millions of
Hindi-speaking users who seek spiritual guidance daily.

**Interview answer:**
"I built Shruti — a multilingual RAG system over the Bhagavad Gita
and Shiv Mahapuran teachings. The key challenge was semantic search
across Hindi and English in the same vector space. I used the
paraphrase-multilingual-MiniLM-L12-v2 model which embeds both
languages in the same 384-dimensional space — so a user typing
'main bahut pareshan hoon' finds the same relevant teachings as
someone typing 'I am very stressed'. The system strictly grounds
its responses in retrieved context, which minimizes hallucination
in a domain where accuracy of scriptural citations matters deeply."

---

## 15. DISCLAIMER TO INCLUDE IN APP

"श्रुति एक AI आधारित आध्यात्मिक सहायक है। यह Shiv Mahapuran
और Bhagavad Gita की शिक्षाओं पर आधारित मार्गदर्शन देता है।
गंभीर स्वास्थ्य, कानूनी, या मानसिक समस्याओं के लिए कृपया
योग्य विशेषज्ञ से परामर्श लें।

Shruti is an AI spiritual assistant based on the teachings of
Shiv Mahapuran and Bhagavad Gita. For serious health, legal,
or mental health concerns, please consult a qualified professional."

---

*हर हर महादेव 🙏*
*Build this. Deploy this. Let it reach the people who need it.*

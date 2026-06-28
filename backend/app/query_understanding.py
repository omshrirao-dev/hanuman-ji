"""
Query Processor step (per spec section 6): romanized Hinglish embeds poorly
in paraphrase-multilingual-MiniLM-L12-v2 (it was trained on Devanagari Hindi
+ English parallel text, not Latin-script Hindi) — measured at 1/10 on the
retrieval test set. Rather than pure-embed the raw query, a small fast LLM
call first turns whatever the user typed into a short English gloss of
their emotional state and situation, which IS something the embedding
model can match well against the English-tagged emotions/life_situations
fields in the knowledge base.
"""
from groq import Groq

REWRITE_MODEL = "llama-3.1-8b-instant"

REWRITE_PROMPT = """The user wrote this message, possibly in Hindi, English, or Hinglish:

"{query}"

In one short English sentence, describe their emotional state and life situation \
for the purpose of searching a spiritual-wisdom knowledge base. Do not answer them, \
do not add commentary — output only the one sentence.

Example:
Input: "naukri nahi mil rahi, bahut tension hai"
Output: Feeling hopeless and stressed about being unable to find a job.

Output:"""


def rewrite_query_for_retrieval(client: Groq, query: str) -> str:
    completion = client.chat.completions.create(
        model=REWRITE_MODEL,
        messages=[{"role": "user", "content": REWRITE_PROMPT.format(query=query)}],
        temperature=0.2,
        max_tokens=60,
    )
    rewritten = completion.choices[0].message.content.strip()
    return rewritten or query

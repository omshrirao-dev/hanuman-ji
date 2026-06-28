"""
Builds gita_shlokas.json from the raw gita/gita dataset (data/raw/gita/*.json).
Every verse gets chapter-level emotions/life_situations/core_lesson as a baseline
so all 700+ shlokas are retrievable. A curated subset of the most pivotal verses
(concentrated in chapters 2, 3, 6, 11, 18 per the build spec, plus a handful of
universally-cited verses elsewhere) gets deeper, verse-specific overrides.
"""
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "..", "raw", "gita")
OUT = os.path.join(BASE, "gita_shlokas.json")

HINDI_AUTHOR_ID = 1     # Swami Ramsukhdas — simple, clear Hindi
ENGLISH_AUTHOR_ID = 16  # Swami Sivananda — accessible English

CHAPTER_META = {
    1: dict(
        emotions=["grief", "fear", "moral confusion", "despair"],
        life_situations=["facing a difficult decision", "fear of conflict with loved ones", "paralysis before a big choice"],
        core_lesson="Even the mightiest can be paralyzed by grief and attachment when facing a hard duty — this is where the Gita's wisdom begins."),
    2: dict(
        emotions=["confusion", "grief", "anxiety about outcomes", "indecision"],
        life_situations=["loss of a loved one", "career setback", "being told to act without knowing the result", "existential doubt"],
        core_lesson="The eternal self is never born and never dies; do your duty without attachment to results."),
    3: dict(
        emotions=["confusion about duty", "laziness vs restlessness", "guilt about inaction"],
        life_situations=["questions about work and career", "motivation problems", "wondering whether to renounce responsibilities"],
        core_lesson="Selfless action performed as duty, without clinging to its fruit, purifies and liberates."),
    4: dict(
        emotions=["doubt about divine justice", "longing for guidance", "confusion about right action"],
        life_situations=["feeling the world is unjust", "questioning whether God intervenes in hard times", "seeking renewal of faith"],
        core_lesson="Whenever righteousness declines, the divine manifests to restore balance — and right knowledge burns away the bondage of past action."),
    5: dict(
        emotions=["torn between renunciation and engagement", "restlessness about life choices"],
        life_situations=["deciding between withdrawing from the world or continuing to work", "burnout"],
        core_lesson="Renunciation and selfless action lead to the same peace — the goal is doing one's work without selfish attachment, not abandoning it."),
    6: dict(
        emotions=["restlessness", "difficulty focusing", "mental agitation", "longing for inner peace"],
        life_situations=["stress and overthinking", "trouble meditating or sitting still", "wanting a daily practice for peace of mind"],
        core_lesson="The mind is your best friend when mastered and your worst enemy when uncontrolled; steady practice and detachment tame it."),
    7: dict(
        emotions=["confusion between the real and the illusory", "searching for meaning"],
        life_situations=["feeling pulled by material distractions", "wanting to distinguish lasting value from fleeting pleasure"],
        core_lesson="Behind the changing material world lies one unchanging divine reality — true knowledge sees through illusion to that source."),
    8: dict(
        emotions=["fear of death", "uncertainty about what comes after", "dread of the unknown"],
        life_situations=["facing death or the death of someone close", "end-of-life questions", "fear about the future"],
        core_lesson="What you remember and dwell on at the moment of death shapes what comes next — so let the mind dwell on the divine now, not later."),
    9: dict(
        emotions=["feeling unworthy", "doubt about whether devotion is enough", "longing to belong spiritually"],
        life_situations=["feeling excluded from spiritual life by background or past mistakes", "wondering if simple devotion counts"],
        core_lesson="Even the smallest offering — a leaf, a flower, water — given with love is fully accepted; devotion has no barrier of worthiness."),
    10: dict(
        emotions=["awe", "wonder", "feeling disconnected from anything greater than oneself"],
        life_situations=["searching for the sacred in ordinary life", "seeking inspiration or a sense of grandeur"],
        core_lesson="The divine is present in the finest expression of everything that exists — greatness anywhere in creation is a glimpse of it."),
    11: dict(
        emotions=["awe", "fear", "overwhelm", "humility before something vast"],
        life_situations=["a profound or overwhelming realization", "feeling small before forces larger than oneself", "a moment of spiritual awakening"],
        core_lesson="Confronted with the vastness of the divine, all human distinctions of strength and control dissolve — surrender, not resistance, is the wise response."),
    12: dict(
        emotions=["longing for closeness with the divine", "love", "devotion", "uncertainty about the path"],
        life_situations=["seeking the simplest path to spiritual peace", "wanting a devotional practice over abstract philosophy"],
        core_lesson="Devotion with a steady, compassionate, contented heart is the most direct path — easier than abstract pursuit of the formless."),
    13: dict(
        emotions=["identity confusion", "feeling lost in roles and labels"],
        life_situations=["questioning who one really is beneath roles and circumstances", "an identity crisis"],
        core_lesson="You are not the body or its circumstances, but the conscious witness within them — knowing this is real knowledge."),
    14: dict(
        emotions=["being pulled in conflicting directions", "mood swings", "frustration with one's own inconsistency"],
        life_situations=["struggling between laziness, restlessness, and clarity", "feeling at the mercy of one's own moods"],
        core_lesson="Three fundamental tendencies — clarity, restlessness, and inertia — drive all behavior; rising above their pull is true freedom."),
    15: dict(
        emotions=["detachment", "searching for ultimate purpose", "feeling rootless or disconnected from source"],
        life_situations=["questioning material attachment", "seeking what is permanent amid constant change"],
        core_lesson="Every being is an eternal fragment of the divine — remembering this dissolves rootlessness and excessive attachment to the material."),
    16: dict(
        emotions=["moral struggle", "anger", "temptation", "disgust at greed or cruelty around oneself"],
        life_situations=["facing temptation or negative influence", "distinguishing good company from harmful company", "battling one's own anger or greed"],
        core_lesson="Lust, anger, and greed are the three gates to self-destruction — recognizing and renouncing them is the gateway to a clear conscience."),
    17: dict(
        emotions=["doubt about the sincerity of one's own practice", "confusion about right versus performative faith"],
        life_situations=["questioning whether one's spiritual practice is genuine", "comparing one's faith to others'"],
        core_lesson="The nature of one's faith shapes the nature of one's character — faith rooted in clarity uplifts; faith rooted in ego or fear does not."),
    18: dict(
        emotions=["final surrender", "seeking ultimate clarity", "relief after long struggle", "liberation from doubt"],
        life_situations=["the end of a long inner struggle", "needing final clarity before a big decision", "wanting to fully let go and trust"],
        core_lesson="Surrendering all results to the divine while doing one's sincere duty is the highest freedom — think it through fully, then act as you decide."),
}

PRIORITY_VERSES = {
    "2.14": dict(
        emotions=["impatience with hardship", "fear of pain", "restlessness"],
        life_situations=["going through a painful or uncomfortable phase of life", "waiting for difficult circumstances to pass"],
        core_lesson="Pleasure and pain, like seasons, are temporary and pass — endure them with steadiness rather than being shaken by either.",
        practical_action="Remind yourself today that the discomfort you're feeling is temporary — practice sitting with it rather than reacting."),
    "2.20": dict(
        emotions=["grief", "fear of death", "fear of loss"],
        life_situations=["grieving the death of someone close", "facing one's own mortality or serious illness"],
        core_lesson="The soul is never born and never dies — it is eternal, so death is not the annihilation it appears to be.",
        practical_action="If you're grieving, sit quietly for a moment and reflect that what made your loved one who they were was never just the body."),
    "2.47": dict(
        emotions=["frustration", "hopelessness", "anxiety about results", "career failure"],
        life_situations=["career failure", "job search", "results not coming despite effort", "feeling discouraged by outcomes outside your control"],
        core_lesson="You have the right to perform your duty, never to its fruits — act fully, but release your grip on the outcome.",
        practical_action="Do your work today with full effort, then consciously let go of worrying about the result."),
    "2.56": dict(
        emotions=["emotional volatility", "being overwhelmed by joy or sorrow"],
        life_situations=["riding an emotional rollercoaster", "wanting more emotional stability"],
        core_lesson="One whose mind stays undisturbed in sorrow, free from craving in joy, and beyond attachment, fear and anger has attained steady wisdom.",
        practical_action="The next time you feel a strong emotional swing today, pause and name it without immediately acting on it."),
    "2.62": dict(
        emotions=["anger", "obsession", "loss of self-control"],
        life_situations=["fixating on a desire or grudge", "feeling controlled by anger"],
        core_lesson="Dwelling on an object breeds attachment; attachment breeds desire, and frustrated desire breeds anger that clouds judgment.",
        practical_action="If you're fixated on something or someone today, notice the chain — attachment leading to desire leading to anger — before it escalates."),
    "2.70": dict(
        emotions=["overwhelm from many desires", "longing for inner stillness"],
        life_situations=["feeling pulled in many directions by wants and obligations", "wanting unshakeable inner peace"],
        core_lesson="Just as rivers enter the ocean without disturbing it, a person of peace lets desires arise without being shaken by them.",
        practical_action="Practice letting one desire or worry today \"enter and pass\" without reacting to it, like a river entering the sea."),
    "3.19": dict(
        emotions=["confusion about duty", "resentment about obligations"],
        life_situations=["doing required work that feels burdensome", "wanting to find meaning in routine duty"],
        core_lesson="Perform your duty without attachment — this, done consistently, leads to the highest good.",
        practical_action="Pick one obligation today and do it fully, without resentment about having to do it."),
    "3.21": dict(
        emotions=["sense of responsibility", "pressure of being a role model"],
        life_situations=["being a parent, leader, or elder others look up to", "worrying about setting a bad example"],
        core_lesson="Whatever a respected person does, others follow — the standard you set becomes the standard others live by.",
        practical_action="Today, act the way you'd want someone who looks up to you to act, since they likely are watching."),
    "3.35": dict(
        emotions=["self-doubt", "comparison with others", "feeling inadequate"],
        life_situations=["comparing your path or career to someone else's", "feeling like you should be doing something different"],
        core_lesson="It is better to imperfectly fulfill your own duty than to perfectly perform someone else's — your own path, even flawed, is safer than someone else's.",
        practical_action="Stop comparing your path to someone else's today — focus only on doing your own work a little better."),
    "4.7": dict(
        emotions=["disillusionment", "anger at injustice", "loss of faith in fairness"],
        life_situations=["witnessing injustice or moral decline around you", "feeling like good values are losing ground"],
        core_lesson="Whenever righteousness declines and unrighteousness rises, the divine takes form to restore balance.",
        practical_action="If the state of the world is weighing on you today, trust that balance is restored over time, even when it's not visible yet."),
    "4.8": dict(
        emotions=["hope amid disillusionment", "longing for justice or relief"],
        life_situations=["waiting for things to get better", "feeling that good people and good causes need protecting"],
        core_lesson="The divine incarnates age after age to protect the good and dissolve what is harmful, re-establishing dharma.",
        practical_action="Hold onto hope today that protection and justice arrive even when the timing isn't yours to control."),
    "6.5": dict(
        emotions=["self-criticism", "feeling like one's own worst enemy"],
        life_situations=["self-sabotage", "negative self-talk", "struggling with self-discipline"],
        core_lesson="One must lift oneself by one's own mind — the mind, depending on how it's used, is either your friend or your enemy.",
        practical_action="Notice one piece of self-critical inner talk today and consciously replace it with something a friend would say to you."),
    "6.6": dict(
        emotions=["inner conflict", "lack of self-mastery"],
        life_situations=["struggling with bad habits", "wanting better self-control"],
        core_lesson="For one who has conquered the mind, it is the best of friends; for one who hasn't, it acts like the worst enemy.",
        practical_action="Pick one small habit today and practice choosing the disciplined response instead of the impulsive one."),
    "6.16": dict(
        emotions=["imbalance", "extremes in lifestyle", "burnout or excess"],
        life_situations=["overworking or under-resting", "extreme dieting, sleep, or lifestyle habits"],
        core_lesson="Yoga is not for one who eats too much or too little, sleeps too much or too little — balance is essential.",
        practical_action="Check one area of your routine today — eating, sleeping, working — and nudge it back toward moderation."),
    "6.35": dict(
        emotions=["frustration with a restless mind", "doubt that meditation is even possible for oneself"],
        life_situations=["finding meditation difficult", "feeling like your mind is too restless for spiritual practice"],
        core_lesson="The restless mind is undoubtedly hard to control, but it is mastered through steady practice and detachment.",
        practical_action="If meditation feels impossible, commit to just two minutes today — practice, not perfection, is the path."),
    "9.22": dict(
        emotions=["worry about being provided for", "anxiety about the future"],
        life_situations=["financial insecurity", "feeling unsupported or alone in providing for yourself"],
        core_lesson="For those who worship with single-minded devotion, the divine personally provides what they lack and preserves what they have.",
        practical_action="If you're anxious about provision today, take the practical step you can — and let go of the rest with trust."),
    "9.26": dict(
        emotions=["feeling unworthy of grace", "doubt that simple devotion is enough"],
        life_situations=["feeling you have too little to offer spiritually", "wanting a simple, accessible practice"],
        core_lesson="Whoever offers a leaf, flower, fruit or even water with love and devotion — that offering is fully accepted.",
        practical_action="Offer one small, sincere gesture of devotion today — its simplicity doesn't diminish its value."),
    "11.32": dict(
        emotions=["awe", "fear", "feeling powerless before forces larger than oneself"],
        life_situations=["facing an outcome that feels inevitable or larger than your control", "witnessing destruction or major upheaval"],
        core_lesson="Time itself moves all things forward regardless of human will — what must unfold will unfold; right action still matters within that.",
        practical_action="When facing something that feels inevitable today, focus on the part you can still influence rather than the part you can't."),
    "11.33": dict(
        emotions=["self-doubt about one's role", "feeling like a small player in big events"],
        life_situations=["being asked to act in a situation much bigger than yourself", "doubting whether your contribution matters"],
        core_lesson="Be merely the instrument — the larger outcome is already set in motion; your part is to act with sincerity, not to claim full authorship.",
        practical_action="Do your part today fully, without needing to carry the weight of the entire outcome on your own shoulders."),
    "12.13": dict(
        emotions=["resentment", "difficulty being compassionate under stress"],
        life_situations=["struggling to stay kind under pressure", "wanting to become a calmer, more compassionate person"],
        core_lesson="One who is free of ill will, friendly and compassionate to all, free from possessiveness and ego, balanced in pain and pleasure, is dear to the divine.",
        practical_action="Practice one act of warmth today toward someone you'd normally feel irritation or indifference toward."),
    "12.14": dict(
        emotions=["restlessness", "discontentment", "self-doubt about spiritual progress"],
        life_situations=["wanting more contentment in daily life", "feeling like you're never doing enough spiritually"],
        core_lesson="One who is content, self-controlled, firm in conviction, with mind and heart fixed on the divine — that devotee is dear to God.",
        practical_action="Find one thing today to feel genuinely content about, instead of reaching for the next thing."),
    "15.7": dict(
        emotions=["feeling disconnected or rootless", "identity confusion"],
        life_situations=["feeling cut off from meaning or source", "an identity or belonging crisis"],
        core_lesson="Every living being is an eternal fragment of the divine — you are never truly disconnected from that source, however far it feels.",
        practical_action="When you feel disconnected today, recall that the very awareness experiencing the disconnection is itself never separate from the source."),
    "16.21": dict(
        emotions=["anger", "greed", "temptation", "self-destructive impulse"],
        life_situations=["battling anger or greed", "facing temptation toward something self-destructive"],
        core_lesson="Lust, anger and greed are the three gates to self-destruction — recognizing them as a trio of warning signs helps you step back before acting.",
        practical_action="Name which of the three — lust, anger, or greed — is driving a current urge, before deciding how to act on it."),
    "18.63": dict(
        emotions=["indecision", "wanting reassurance before a big choice"],
        life_situations=["standing at a major crossroads", "needing to make up your own mind after receiving advice"],
        core_lesson="Reflect fully on this wisdom, then do as you decide — the choice, ultimately, is yours to make.",
        practical_action="After weighing the guidance you've received on a decision, give yourself permission today to actually decide."),
    "18.66": dict(
        emotions=["guilt", "fear of past mistakes", "longing for a clean start"],
        life_situations=["carrying guilt over past wrongs", "wanting to start fresh", "fear of being beyond forgiveness"],
        core_lesson="Abandon all other refuges and surrender to the divine alone — you will be released from all sin; do not grieve.",
        practical_action="If guilt from the past is weighing on you, practice surrendering it today instead of carrying it alone."),
    "18.78": dict(
        emotions=["hope", "resolve", "renewed confidence after doubt"],
        life_situations=["concluding a long period of confusion or crisis", "needing reassurance that clarity and right action lead somewhere good"],
        core_lesson="Wherever there is the union of right guidance and willing action, there is certain victory, prosperity and steadfast resolve.",
        practical_action="Carry the resolve you've built today into your next decision, trusting that clarity plus sincere effort leads somewhere good."),
}


def clean_sanskrit(text: str) -> str:
    text = re.sub(r"।?।\s*\d+\.\d+\s*।?।", "", text)
    text = re.sub(r"\.\.\s*\d+\.\d+\s*\.\.", "", text)
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    return "\n".join(lines)


def clean_text(text: str) -> str:
    text = re.sub(r"^\s*।?।\s*\d+\.\d+\s*।?।\s*", "", text or "")
    return re.sub(r"\s+", " ", text).strip()


def main():
    with open(os.path.join(RAW, "verse.json"), encoding="utf-8") as f:
        verses = json.load(f)
    with open(os.path.join(RAW, "translation.json"), encoding="utf-8") as f:
        translations = json.load(f)
    with open(os.path.join(RAW, "chapters.json"), encoding="utf-8") as f:
        chapters = json.load(f)

    chapters_by_num = {c["chapter_number"]: c for c in chapters}
    trans_by_key = {}
    for t in translations:
        trans_by_key[(t["verse_id"], t["lang"], t["author_id"])] = t["description"]

    out = []
    for v in verses:
        ch_num = v["chapter_number"]
        verse_num = v["verse_number"]
        key = f"{ch_num}.{verse_num}"
        chapter = chapters_by_num[ch_num]
        meta = CHAPTER_META.get(ch_num, {})
        override = PRIORITY_VERSES.get(key)

        hindi = clean_text(trans_by_key.get((v["id"], "hindi", HINDI_AUTHOR_ID), ""))
        english = clean_text(trans_by_key.get((v["id"], "english", ENGLISH_AUTHOR_ID), ""))

        entry = {
            "id": f"BG-{key}",
            "type": "shloka",
            "chapter": ch_num,
            "verse": verse_num,
            "sanskrit": clean_sanskrit(v["text"]),
            "transliteration": clean_text(v.get("transliteration", "")),
            "word_meanings": clean_text(v.get("word_meanings", "")),
            "hindi": hindi,
            "english": english,
            "chapter_name_en": chapter["name_translation"],
            "chapter_name_hi": chapter["name"],
            "chapter_theme": chapter["name_meaning"],
            "emotions": override["emotions"] if override else meta.get("emotions", []),
            "life_situations": override["life_situations"] if override else meta.get("life_situations", []),
            "core_lesson": override["core_lesson"] if override else meta.get("core_lesson", chapter["name_meaning"]),
            "practical_action": override["practical_action"] if override else None,
            "priority": bool(override),
            "source": f"Bhagavad Gita {key} (Hindi: Swami Ramsukhdas; English: Swami Sivananda)",
        }
        out.append(entry)

    out.sort(key=lambda e: (e["chapter"], e["verse"]))
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    n_priority = sum(1 for e in out if e["priority"])
    print(f"Wrote {len(out)} verses to {OUT} ({n_priority} hand-curated priority verses)")


if __name__ == "__main__":
    main()

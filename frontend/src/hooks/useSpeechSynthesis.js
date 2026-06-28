import { useCallback, useEffect, useRef, useState } from "react";

export function useSpeechSynthesis() {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [voicePreference, setVoicePreference] = useState("female");
  const utteranceRef = useRef(null);

  useEffect(() => {
    return () => window.speechSynthesis?.cancel();
  }, []);

  const pickVoice = useCallback(
    (lang) => {
      const voices = window.speechSynthesis?.getVoices() || [];
      const candidates = voices.filter((v) => v.lang?.toLowerCase().startsWith(lang.split("-")[0]));
      if (candidates.length === 0) return null;
      if (voicePreference === "male") {
        return candidates.find((v) => /male/i.test(v.name)) || candidates[0];
      }
      return candidates.find((v) => /female/i.test(v.name)) || candidates[0];
    },
    [voicePreference]
  );

  const speak = useCallback(
    (text, language = "hi") => {
      if (!window.speechSynthesis) return;
      window.speechSynthesis.cancel();

      const lang = language === "hi" || language === "hi-en" ? "hi-IN" : "en-IN";
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = lang;
      utterance.rate = 0.85;
      utterance.pitch = 1.0;
      const voice = pickVoice(lang);
      if (voice) utterance.voice = voice;

      utterance.onstart = () => setIsSpeaking(true);
      utterance.onend = () => setIsSpeaking(false);
      utterance.onerror = () => setIsSpeaking(false);

      utteranceRef.current = utterance;
      window.speechSynthesis.speak(utterance);
    },
    [pickVoice]
  );

  const stop = useCallback(() => {
    window.speechSynthesis?.cancel();
    setIsSpeaking(false);
  }, []);

  return {
    isSupported: typeof window !== "undefined" && "speechSynthesis" in window,
    isSpeaking,
    speak,
    stop,
    voicePreference,
    setVoicePreference,
  };
}

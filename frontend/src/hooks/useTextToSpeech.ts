import { useState, useEffect } from 'react';

interface UseTextToSpeechReturn {
  speak: (text: string, options?: SpeechSynthesisUtteranceOptions) => void;
  stop: () => void;
  pause: () => void;
  resume: () => void;
  isSpeaking: boolean;
  isPaused: boolean;
  isSupported: boolean;
}

interface SpeechSynthesisUtteranceOptions {
  lang?: string;
  rate?: number;
  pitch?: number;
  volume?: number;
}

/**
 * Custom hook for text-to-speech using Web Speech API
 * Works in all modern browsers
 */
export const useTextToSpeech = (): UseTextToSpeechReturn => {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isPaused, setIsPaused] = useState(false);

  // Check if Speech Synthesis is supported
  const isSupported = 'speechSynthesis' in window;

  useEffect(() => {
    if (!isSupported) return;

    const handleStart = () => setIsSpeaking(true);
    const handleEnd = () => {
      setIsSpeaking(false);
      setIsPaused(false);
    };
    const handlePause = () => setIsPaused(true);
    const handleResume = () => setIsPaused(false);

    // Add event listeners to track speaking state
    window.speechSynthesis.addEventListener?.('start' as any, handleStart);
    window.speechSynthesis.addEventListener?.('end' as any, handleEnd);
    window.speechSynthesis.addEventListener?.('pause' as any, handlePause);
    window.speechSynthesis.addEventListener?.('resume' as any, handleResume);

    return () => {
      window.speechSynthesis.cancel();
      window.speechSynthesis.removeEventListener?.('start' as any, handleStart);
      window.speechSynthesis.removeEventListener?.('end' as any, handleEnd);
      window.speechSynthesis.removeEventListener?.('pause' as any, handlePause);
      window.speechSynthesis.removeEventListener?.('resume' as any, handleResume);
    };
  }, [isSupported]);

  const speak = (text: string, options: SpeechSynthesisUtteranceOptions = {}) => {
    if (!isSupported) {
      console.error('Text-to-speech is not supported in this browser');
      return;
    }

    // Cancel any ongoing speech
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = options.lang || 'de-DE'; // German by default
    utterance.rate = options.rate || 1.0;
    utterance.pitch = options.pitch || 1.0;
    utterance.volume = options.volume || 1.0;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => {
      setIsSpeaking(false);
      setIsPaused(false);
    };
    utterance.onerror = (event) => {
      console.error('Speech synthesis error:', event);
      setIsSpeaking(false);
      setIsPaused(false);
    };

    window.speechSynthesis.speak(utterance);
  };

  const stop = () => {
    if (isSupported) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      setIsPaused(false);
    }
  };

  const pause = () => {
    if (isSupported && isSpeaking) {
      window.speechSynthesis.pause();
      setIsPaused(true);
    }
  };

  const resume = () => {
    if (isSupported && isPaused) {
      window.speechSynthesis.resume();
      setIsPaused(false);
    }
  };

  return {
    speak,
    stop,
    pause,
    resume,
    isSpeaking,
    isPaused,
    isSupported,
  };
};

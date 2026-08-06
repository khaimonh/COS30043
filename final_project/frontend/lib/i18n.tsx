"use client";

import {
  createContext,
  useContext,
  useSyncExternalStore,
  type ReactNode,
} from "react";

import { en, type Dict } from "./i18n/en";
import { vi } from "./i18n/vi";

export type Lang = "en" | "vi";

const dicts: Record<Lang, Dict> = { en, vi };
const STORAGE_KEY = "fluxus-lang";
const LANG_EVENT = "fluxus-lang-change";

type Ctx = {
  lang: Lang;
  setLang: (lang: Lang) => void;
  t: (key: keyof Dict) => string;
  tf: (key: keyof Dict, vars: Record<string, string | number>) => string;
};

const LanguageContext = createContext<Ctx>({
  lang: "en",
  setLang: () => {},
  t: (key) => en[key],
  tf: (key, vars) => interpolate(en[key], vars),
});

function interpolate(template: string, vars: Record<string, string | number>) {
  return template.replace(/\{(\w+)\}/g, (_, k: string) => String(vars[k] ?? `{${k}}`));
}

function readLang(): Lang {
  if (typeof window === "undefined") return "en";
  const saved = localStorage.getItem(STORAGE_KEY);
  return saved === "en" || saved === "vi" ? saved : "en";
}

function subscribeLang(callback: () => void) {
  window.addEventListener(LANG_EVENT, callback);
  return () => window.removeEventListener(LANG_EVENT, callback);
}

export function LanguageProvider({ children }: { children: ReactNode }) {
  const lang = useSyncExternalStore<Lang>(subscribeLang, readLang, () => "en");

  const setLang = (next: Lang) => {
    localStorage.setItem(STORAGE_KEY, next);
    window.dispatchEvent(new Event(LANG_EVENT));
  };

  const t = (key: keyof Dict) => dicts[lang][key] ?? en[key];
  const tf = (key: keyof Dict, vars: Record<string, string | number>) =>
    interpolate(dicts[lang][key], vars);

  return (
    <LanguageContext.Provider value={{ lang, setLang, t, tf }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLang() {
  return useContext(LanguageContext);
}

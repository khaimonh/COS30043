import { ref, type Ref } from "vue";
import { en, type Dict } from "./en";
import { vi } from "./vi";

export type Lang = "en" | "vi";

const STORAGE_KEY = "fluxus-lang";

function readLang(): Lang {
  if (typeof localStorage !== "undefined") {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored === "en" || stored === "vi") return stored;
  }
  return "en";
}

export const lang: Ref<Lang> = ref(readLang());

const dictionaries: Record<Lang, Dict> = { en, vi };

export function setLang(next: Lang): void {
  lang.value = next;
  localStorage.setItem(STORAGE_KEY, next);
}

export function t(key: keyof Dict): string {
  return dictionaries[lang.value][key];
}

export function tf(key: keyof Dict, vars: Record<string, string | number>): string {
  let out = dictionaries[lang.value][key];
  for (const [name, value] of Object.entries(vars)) {
    out = out.replace(`{${name}}`, String(value));
  }
  return out;
}

export function useI18n() {
  return { lang, setLang, t, tf };
}

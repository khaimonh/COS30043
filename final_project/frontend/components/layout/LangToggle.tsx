"use client";

import { useLang } from "@/lib/i18n";

const options = [
  { code: "en", label: "EN" },
  { code: "vi", label: "VI" },
] as const;

export function LangToggle() {
  const { lang, setLang } = useLang();

  return (
    <div
      className="inline-flex items-center rounded-full border border-border bg-surface p-0.5"
      role="group"
      aria-label="Language"
    >
      {options.map((opt) => (
        <button
          key={opt.code}
          type="button"
          onClick={() => setLang(opt.code)}
          aria-pressed={lang === opt.code}
          className={`rounded-full px-3 py-1 font-mono text-xs font-medium transition-colors duration-150 ${
            lang === opt.code
              ? "bg-accent text-white"
              : "text-muted hover:text-foreground"
          }`}
        >
          {opt.label}
        </button>
      ))}
    </div>
  );
}

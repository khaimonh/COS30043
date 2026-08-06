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
      className="inline-flex items-center rounded-lg border border-border bg-surface p-0.5"
      role="group"
      aria-label="Language"
    >
      {options.map((opt) => (
        <button
          key={opt.code}
          type="button"
          onClick={() => setLang(opt.code)}
          aria-pressed={lang === opt.code}
          className={`rounded-md px-2.5 py-1 text-xs font-medium transition-colors ${
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

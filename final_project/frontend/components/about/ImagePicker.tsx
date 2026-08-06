"use client";

import { useState } from "react";
import Image from "next/image";
import { useLang } from "@/lib/i18n";

const scenes = [
  { key: "mountain", src: "/images/mountain.svg", label: "about.mountain", alt: "about.mountainAlt" },
  { key: "ocean", src: "/images/ocean.svg", label: "about.ocean", alt: "about.oceanAlt" },
] as const;

export function ImagePicker() {
  const { t } = useLang();
  const [scene, setScene] = useState<string>("mountain");
  const selected = scenes.find((s) => s.key === scene) ?? scenes[0];

  return (
    <div>
      <div className="grid gap-3 sm:grid-cols-2" role="radiogroup" aria-label={t("about.sceneTitle")}>
        {scenes.map((s) => (
          <label key={s.key} className="cursor-pointer">
            <input
              type="radio"
              name="scene"
              value={s.key}
              checked={scene === s.key}
              onChange={() => setScene(s.key)}
              className="peer sr-only"
            />
            <span className="block rounded-xl border border-border bg-surface px-4 py-3 text-sm font-medium text-muted transition-colors peer-checked:border-accent peer-checked:bg-accent-soft peer-checked:text-accent-hover">
              {t(s.label)}
            </span>
          </label>
        ))}
      </div>
      <div className="mt-6">
        <Image
          src={selected.src}
          alt={t(selected.alt)}
          width={800}
          height={500}
          className="w-full rounded-xl border border-border"
        />
      </div>
    </div>
  );
}

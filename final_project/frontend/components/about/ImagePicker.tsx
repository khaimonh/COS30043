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
      <div role="radiogroup" aria-label={t("about.sceneTitle")}>
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
            <span className="mr-4 inline-block py-1 font-mono text-sm text-muted underline decoration-border decoration-1 underline-offset-8 transition-colors duration-150 hover:text-foreground peer-checked:text-foreground peer-checked:decoration-accent">
              {t(s.label)}
            </span>
          </label>
        ))}
      </div>
      <div className="mt-8">
        <Image
          src={selected.src}
          alt={t(selected.alt)}
          width={800}
          height={500}
          className="w-full rounded-2xl border border-border"
        />
      </div>
    </div>
  );
}

"use client";

import { useLang } from "@/lib/i18n";
import { GreetingForm } from "@/components/about/GreetingForm";
import { ImagePicker } from "@/components/about/ImagePicker";

export default function About() {
  const { t } = useLang();

  return (
    <div className="mx-auto w-full max-w-6xl px-4 pb-20 pt-10 sm:px-6 sm:pt-14">
      <div className="max-w-[50ch]">
        <p className="font-display text-3xl font-semibold tracking-tight sm:text-4xl">
          {t("about.salutation")}
        </p>
        <p className="mt-8 text-lg leading-relaxed text-muted">{t("about.paragraph")}</p>
      </div>

      <div className="mt-16 max-w-[50ch]">
        <h2 className="text-xl font-semibold tracking-tight">{t("about.formTitle")}</h2>
        <p className="mt-2 font-mono text-sm text-muted">{t("about.ps")}</p>
        <div className="mt-8">
          <GreetingForm />
        </div>
      </div>

      <div className="mt-16 max-w-[50ch]">
        <h2 className="text-xl font-semibold tracking-tight">{t("about.sceneTitle")}</h2>
        <p className="mt-2 font-mono text-sm text-muted">{t("about.welcomeHint")}</p>
        <div className="mt-8">
          <ImagePicker />
        </div>
      </div>
    </div>
  );
}

"use client";

import Image from "next/image";
import { useLang } from "@/lib/i18n";
import { ButtonLink } from "@/components/ui/Button";

export function PreviewBand() {
  const { t } = useLang();

  return (
    <section className="mx-auto w-full max-w-6xl px-4 pb-20 sm:px-6 sm:pb-24">
      <div className="grid items-center gap-10 lg:grid-cols-2 lg:gap-14">
        <Image
          src="/images/dashboard-preview.svg"
          alt={t("home.image2Alt")}
          width={800}
          height={480}
          className="w-full rounded-2xl border border-border bg-surface"
        />
        <div>
          <h2 className="max-w-[22ch] text-3xl font-semibold tracking-tight sm:text-4xl">
            {t("home.ctaStripTitle")}
          </h2>
          <p className="mt-4 max-w-[45ch] leading-relaxed text-muted">
            {t("home.ctaStripNote")}
          </p>
          <ButtonLink href="/news" size="lg" className="mt-9">
            {t("home.ctaPrimary")}
          </ButtonLink>
        </div>
      </div>
    </section>
  );
}

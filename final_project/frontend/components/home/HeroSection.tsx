"use client";

import Image from "next/image";
import { useLang } from "@/lib/i18n";
import { Badge } from "@/components/ui/Badge";
import { ButtonLink } from "@/components/ui/Button";

export function HeroSection() {
  const { t } = useLang();

  return (
    <div className="border-b border-border">
      <div className="mx-auto grid w-full max-w-6xl items-center gap-10 px-4 py-16 sm:px-6 sm:py-24 lg:grid-cols-2 lg:gap-14">
        <div>
          <Badge variant="accent">{t("home.badge")}</Badge>
          <h1 className="mt-5 text-4xl font-bold leading-tight tracking-tight text-foreground sm:text-5xl">
            {t("home.title")}
          </h1>
          <p className="mt-6 max-w-xl text-base leading-relaxed text-muted sm:text-lg">
            {t("home.welcome")}
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <ButtonLink href="/news" size="lg">
              {t("home.ctaPrimary")}
            </ButtonLink>
            <ButtonLink href="/about" size="lg" variant="outline">
              {t("home.ctaSecondary")}
            </ButtonLink>
          </div>
        </div>

        <div className="relative">
          <div className="absolute -inset-4 rounded-3xl bg-accent/10 blur-2xl" aria-hidden />
          <Image
            src="/images/hero-chart.svg"
            alt={t("home.image1Alt")}
            width={800}
            height={480}
            priority
            className="relative w-full rounded-2xl border border-border shadow-2xl shadow-black/40"
          />
        </div>
      </div>
    </div>
  );
}

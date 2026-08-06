"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import { useLang } from "@/lib/i18n";
import { ButtonLink } from "@/components/ui/Button";

function useCountUp(target: number, duration = 400) {
  const [value, setValue] = useState(0);

  useEffect(() => {
    let raf: number;
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const start = performance.now();
    const step = (now: number) => {
      const p = reduce ? 1 : Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - p, 3);
      setValue(Math.round(eased * target));
      if (p < 1) raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
  }, [target, duration]);

  return value;
}

export function HeroSection() {
  const { t } = useLang();
  const count = useCountUp(500);

  return (
    <section className="mx-auto w-full max-w-6xl px-4 pb-16 pt-10 sm:px-6 sm:pb-24 sm:pt-14">
      <div className="grid items-center gap-12 lg:grid-cols-[minmax(0,1.1fr)_minmax(0,0.9fr)] lg:gap-16">
        <div>
          <p className="font-mono text-xs uppercase tracking-[0.14em] text-accent-hover">
            {t("home.heroTag")}
          </p>
          <p className="mt-6 font-display text-[clamp(4rem,16vw,10.5rem)] font-semibold leading-[0.9] tracking-[-0.04em] tabular-nums">
            <span aria-hidden>{count.toLocaleString("en-US")}</span>
            <span className="sr-only">{t("home.heroFigure")}</span>
            <span className="ml-3 align-top font-mono text-[0.32em] font-medium tracking-normal text-muted">
              {t("home.stat2Label")}
            </span>
          </p>
          <h1 className="mt-8 max-w-[22ch] text-[clamp(2.5rem,5vw,4.25rem)] font-semibold leading-[1.02] tracking-[-0.03em]">
            {t("home.title")}
          </h1>
          <p className="mt-6 max-w-[65ch] text-base leading-relaxed text-muted sm:text-lg">
            {t("home.welcome")}
          </p>
          <div className="mt-10 flex flex-wrap items-center gap-4">
            <ButtonLink href="/news" size="lg">
              {t("home.ctaPrimary")}
            </ButtonLink>
            <ButtonLink href="/about" size="lg" variant="outline">
              {t("home.ctaSecondary")}
            </ButtonLink>
          </div>
        </div>

        <div className="relative">
          <div
            className="absolute -inset-6 rounded-3xl bg-accent-soft blur-3xl"
            aria-hidden
          />
          <Image
            src="/images/hero-chart.svg"
            alt={t("home.image1Alt")}
            width={800}
            height={480}
            priority
            className="relative w-full rounded-2xl border border-border bg-surface"
          />
        </div>
      </div>
    </section>
  );
}

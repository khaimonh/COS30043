"use client";

import Link from "next/link";
import { useLang } from "@/lib/i18n";

const links = [
  { href: "/", key: "nav.home" },
  { href: "/about", key: "nav.about" },
  { href: "/news", key: "nav.news" },
] as const;

export function Footer() {
  const { t, tf } = useLang();

  return (
    <footer className="border-t border-border">
      <div className="mx-auto w-full max-w-6xl px-4 py-16 sm:px-6 sm:py-20">
        <p className="max-w-[28ch] text-[clamp(1.75rem,5vw,3.25rem)] font-semibold leading-[1.05] tracking-[-0.03em]">
          {t("footer.statement")}
        </p>
        <div className="mt-10 flex flex-col gap-4 border-t border-border pt-5 text-sm sm:flex-row sm:items-baseline sm:justify-between">
          <span className="font-mono text-foreground">Fluxus</span>
          <nav className="flex flex-wrap gap-x-5 gap-y-2" aria-label="Footer">
            {links.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="text-muted transition-colors duration-150 hover:text-foreground"
              >
                {t(link.key)}
              </Link>
            ))}
          </nav>
          <span className="font-mono text-xs text-muted">
            {tf("footer.rights", { year: String(new Date().getFullYear()) })}
          </span>
        </div>
      </div>
    </footer>
  );
}

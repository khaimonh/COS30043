"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

import { useLang } from "@/lib/i18n";
import { ButtonLink } from "@/components/ui/Button";
import { LangToggle } from "./LangToggle";

const links = [
  { href: "/", key: "nav.home" },
  { href: "/about", key: "nav.about" },
  { href: "/news", key: "nav.news" },
] as const;

function Brand() {
  return (
    <Link href="/" className="flex items-center gap-2.5">
      <span className="grid h-7 w-7 place-items-center rounded-full bg-accent">
        <svg viewBox="0 0 24 24" className="h-4 w-4 text-white" aria-hidden>
          <rect x="4" y="9" width="3" height="9" rx="0.5" fill="currentColor" />
          <rect x="10.5" y="4" width="3" height="14" rx="0.5" fill="currentColor" />
          <rect x="17" y="7" width="3" height="11" rx="0.5" fill="currentColor" />
        </svg>
      </span>
      <span className="font-mono text-base font-medium tracking-tight text-foreground">
        Fluxus
      </span>
    </Link>
  );
}

export function Navbar() {
  const { t } = useLang();
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  const isActive = (href: string) =>
    href === "/" ? pathname === "/" : pathname.startsWith(href);

  return (
    <header className="fixed inset-x-0 top-4 z-[300] flex justify-center px-4">
      <div className="flex max-w-[720px] items-center gap-1 rounded-full border border-border bg-background/75 py-1.5 pl-2.5 pr-1.5 shadow-float backdrop-blur-xl">
        <Brand />

        <nav className="hidden items-center gap-0.5 lg:flex" aria-label="Main">
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className={`rounded-full px-3 py-1.5 text-sm font-medium transition-colors duration-150 ${
                isActive(link.href)
                  ? "bg-surface-2 text-foreground"
                  : "text-muted hover:text-foreground"
              }`}
            >
              {t(link.key)}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-1.5 pl-1">
          <LangToggle />
          <ButtonLink
            href="/news"
            size="sm"
            className="hidden lg:inline-flex"
          >
            {t("nav.explore")}
          </ButtonLink>
          <button
            type="button"
            className="grid h-9 w-9 place-items-center rounded-full text-muted transition-colors duration-150 hover:text-foreground lg:hidden"
            onClick={() => setOpen((v) => !v)}
            aria-expanded={open}
            aria-label="Toggle menu"
          >
            <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden>
              {open ? (
                <path d="M6 6l12 12M18 6L6 18" strokeLinecap="round" />
              ) : (
                <path d="M4 7h16M4 12h16M4 17h16" strokeLinecap="round" />
              )}
            </svg>
          </button>
        </div>
      </div>

      {open ? (
        <nav
          className="absolute top-full mt-2 w-full max-w-[220px] rounded-2xl border border-border bg-background/90 p-2 shadow-float backdrop-blur-xl lg:hidden"
          aria-label="Mobile"
        >
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              onClick={() => setOpen(false)}
              className={`block rounded-full px-3 py-2.5 text-sm font-medium transition-colors duration-150 ${
                isActive(link.href)
                  ? "bg-surface-2 text-foreground"
                  : "text-muted hover:text-foreground"
              }`}
            >
              {t(link.key)}
            </Link>
          ))}
        </nav>
      ) : null}
    </header>
  );
}

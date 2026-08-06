import type { ReactNode } from "react";
import { Section } from "./Section";

export function PageHeader({
  eyebrow,
  title,
  subtitle,
}: {
  eyebrow?: ReactNode;
  title: ReactNode;
  subtitle?: ReactNode;
}) {
  return (
    <Section className="pt-12 pb-8 sm:pt-16">
      {eyebrow ? (
        <div className="mb-3 font-mono text-xs uppercase tracking-[0.14em] text-accent-hover">
          {eyebrow}
        </div>
      ) : null}
      <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">{title}</h1>
      {subtitle ? <p className="mt-3 max-w-[65ch] text-muted">{subtitle}</p> : null}
    </Section>
  );
}

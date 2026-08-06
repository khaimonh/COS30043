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
        <div className="mb-3 text-sm font-medium uppercase tracking-widest text-accent-hover">
          {eyebrow}
        </div>
      ) : null}
      <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">{title}</h1>
      {subtitle ? <p className="mt-3 max-w-2xl text-muted">{subtitle}</p> : null}
    </Section>
  );
}

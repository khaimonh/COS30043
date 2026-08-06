import type { ReactNode } from "react";

type Variant = "neutral" | "accent";

const variants: Record<Variant, string> = {
  neutral: "border-border bg-surface text-muted",
  accent: "border-accent/40 bg-accent-soft text-accent-hover",
};

export function Badge({
  variant = "neutral",
  className = "",
  children,
}: {
  variant?: Variant;
  className?: string;
  children: ReactNode;
}) {
  return (
    <span
      className={`inline-flex items-center whitespace-nowrap rounded-full border px-2.5 py-0.5 font-mono text-xs font-medium tracking-wide ${variants[variant]} ${className}`}
    >
      {children}
    </span>
  );
}

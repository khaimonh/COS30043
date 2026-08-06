import type { InputHTMLAttributes } from "react";

export function Input({
  className = "",
  ...props
}: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      className={`w-full rounded-lg border border-border bg-surface px-3.5 py-2 text-sm text-foreground placeholder:text-muted transition-colors duration-150 hover:border-muted/50 focus-visible:outline-2 focus-visible:outline-offset-0 focus-visible:outline-focus ${className}`}
      {...props}
    />
  );
}

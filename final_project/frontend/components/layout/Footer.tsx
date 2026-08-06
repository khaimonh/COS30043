export function Footer() {
  return (
    <footer className="border-t border-border">
      <div className="mx-auto flex w-full max-w-6xl flex-col items-center justify-between gap-2 px-4 py-6 text-sm text-muted sm:flex-row sm:px-6">
        <span className="font-medium text-foreground">Fluxus</span>
        <span>© {new Date().getFullYear()} Fluxus — Vietnam stock market playground</span>
      </div>
    </footer>
  );
}

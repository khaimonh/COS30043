"use client";

import { useLang } from "@/lib/i18n";
import { Button } from "@/components/ui/Button";

export function Pagination({
  page,
  totalPages,
  onPage,
}: {
  page: number;
  totalPages: number;
  onPage: (page: number) => void;
}) {
  const { t, tf } = useLang();

  if (totalPages <= 1) return null;

  return (
    <nav
      className="flex items-center justify-between gap-4 border-t border-border pt-5"
      aria-label="pagination"
    >
      <Button
        variant="ghost"
        size="sm"
        onClick={() => onPage(page - 1)}
        disabled={page <= 1}
      >
        {t("news.prev")}
      </Button>
      <span className="font-mono text-xs text-muted">
        {tf("news.pageOf", { page: String(page), total: String(totalPages) })}
      </span>
      <Button
        variant="ghost"
        size="sm"
        onClick={() => onPage(page + 1)}
        disabled={page >= totalPages}
      >
        {t("news.next")}
      </Button>
    </nav>
  );
}

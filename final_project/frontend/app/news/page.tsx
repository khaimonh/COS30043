"use client";

import { useEffect, useMemo, useState } from "react";
import { useLang } from "@/lib/i18n";
import { Section } from "@/components/ui/Section";
import { PageHeader } from "@/components/ui/PageHeader";
import { NewsList } from "@/components/news/NewsList";
import { NewsSearch } from "@/components/news/NewsSearch";
import { Pagination } from "@/components/news/Pagination";
import { matchesSearch, PAGE_SIZE, type NewsItem } from "@/lib/news";

export default function News() {
  const { t, tf } = useLang();
  const [items, setItems] = useState<NewsItem[] | null>(null);
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("");
  const [page, setPage] = useState(1);

  useEffect(() => {
    fetch("/data/news.json")
      .then((res) => res.json())
      .then((data) => setItems(data.items))
      .catch(() => setItems([]));
  }, []);

  const categories = useMemo(
    () => [...new Set((items ?? []).map((i) => i.category))],
    [items]
  );

  const filtered = useMemo(
    () =>
      (items ?? []).filter(
        (item) =>
          matchesSearch(item, query) &&
          (category === "" || item.category === category)
      ),
    [items, query, category]
  );

  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const current = Math.min(page, totalPages);
  const visible = filtered.slice((current - 1) * PAGE_SIZE, current * PAGE_SIZE);

  return (
    <main className="flex-1">
      <PageHeader
        eyebrow={t("brand.name")}
        title={t("news.title")}
        subtitle={t("news.subtitle")}
      />
      <Section className="pb-16 sm:pb-20">
        <div className="mb-8 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div className="max-w-xl flex-1">
            <NewsSearch
              query={query}
              onQueryChange={(value) => {
                setQuery(value);
                setPage(1);
              }}
              category={category}
              onCategoryChange={(value) => {
                setCategory(value);
                setPage(1);
              }}
              categories={categories}
            />
          </div>
          <p className="text-sm text-muted">
            {tf("news.results", { n: String(filtered.length) })}
          </p>
        </div>

        {items === null ? (
          <p className="text-muted">{t("news.loading")}</p>
        ) : visible.length === 0 ? (
          <p className="rounded-xl border border-border bg-surface px-5 py-10 text-center text-muted">
            {t("news.empty")}
          </p>
        ) : (
          <>
            <NewsList items={visible} />
            <div className="mt-10">
              <Pagination page={current} totalPages={totalPages} onPage={setPage} />
            </div>
          </>
        )}
      </Section>
    </main>
  );
}

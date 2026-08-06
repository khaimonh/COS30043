"use client";

import { useEffect, useMemo, useState } from "react";
import { useLang } from "@/lib/i18n";
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
    <div className="mx-auto w-full max-w-6xl px-4 pb-20 pt-10 sm:px-6 sm:pt-14">
      <header className="pb-10">
        <p className="font-mono text-xs uppercase tracking-[0.14em] text-accent-hover">
          {t("brand.name")}
        </p>
        <h1 className="mt-3 text-3xl font-semibold tracking-tight sm:text-4xl">
          {t("news.title")}
        </h1>
        <p className="mt-3 max-w-[65ch] text-muted">{t("news.subtitle")}</p>
      </header>

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
        <p className="font-mono text-xs text-muted">
          {tf("news.results", { n: String(filtered.length) })}
        </p>
      </div>

      {items === null ? (
        <p className="text-muted">{t("news.loading")}</p>
      ) : visible.length === 0 ? (
        <p className="text-muted">{t("news.empty")}</p>
      ) : (
        <>
          <NewsList items={visible} />
          <div className="mt-10">
            <Pagination page={current} totalPages={totalPages} onPage={setPage} />
          </div>
        </>
      )}
    </div>
  );
}

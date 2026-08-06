"use client";

import { useLang } from "@/lib/i18n";
import { Input } from "@/components/ui/Input";
import { Select } from "@/components/ui/Select";

export function NewsSearch({
  query,
  onQueryChange,
  category,
  onCategoryChange,
  categories,
}: {
  query: string;
  onQueryChange: (value: string) => void;
  category: string;
  onCategoryChange: (value: string) => void;
  categories: string[];
}) {
  const { t } = useLang();

  return (
    <div className="grid gap-3 sm:grid-cols-[1fr_220px]">
      <Input
        type="search"
        value={query}
        onChange={(e) => onQueryChange(e.target.value)}
        placeholder={t("news.searchPlaceholder")}
        aria-label={t("news.searchPlaceholder")}
      />
      <Select
        value={category}
        onChange={(e) => onCategoryChange(e.target.value)}
        aria-label={t("news.allCategories")}
      >
        <option value="">{t("news.allCategories")}</option>
        {categories.map((c) => (
          <option key={c} value={c}>
            {c}
          </option>
        ))}
      </Select>
    </div>
  );
}

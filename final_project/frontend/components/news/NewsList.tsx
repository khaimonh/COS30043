import type { NewsItem } from "@/lib/news";
import { NewsCard } from "./NewsCard";

export function NewsList({ items }: { items: NewsItem[] }) {
  return (
    <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
      {items.map((item) => (
        <NewsCard key={item.id} item={item} />
      ))}
    </div>
  );
}

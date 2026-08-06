import type { NewsItem } from "@/lib/news";
import { NewsCard } from "./NewsCard";

export function NewsList({ items }: { items: NewsItem[] }) {
  return (
    <div className="divide-y divide-border">
      {items.map((item) => (
        <NewsCard key={item.id} item={item} />
      ))}
    </div>
  );
}

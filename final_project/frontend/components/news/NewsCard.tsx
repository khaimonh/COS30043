import type { NewsItem } from "@/lib/news";
import { formatDate } from "@/lib/news";
import { Badge } from "@/components/ui/Badge";

export function NewsCard({ item }: { item: NewsItem }) {
  return (
    <article className="py-5">
      <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
        <time className="font-mono text-xs text-muted" dateTime={item.date}>
          {formatDate(item.date)}
        </time>
        <Badge>{item.category}</Badge>
      </div>
      <h3 className="mt-2.5 text-lg font-semibold leading-snug tracking-tight">
        {item.title}
      </h3>
      <p className="mt-2 max-w-[70ch] text-sm leading-relaxed text-muted">
        {item.content}
      </p>
    </article>
  );
}

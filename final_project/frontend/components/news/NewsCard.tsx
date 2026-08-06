import type { NewsItem } from "@/lib/news";
import { formatDate } from "@/lib/news";
import { Badge } from "@/components/ui/Badge";
import { Card, CardBody } from "@/components/ui/Card";

export function NewsCard({ item }: { item: NewsItem }) {
  return (
    <Card className="h-full">
      <CardBody className="flex h-full flex-col">
        <div className="flex items-center gap-3">
          <time className="text-sm text-muted" dateTime={item.date}>
            {formatDate(item.date)}
          </time>
          <Badge>{item.category}</Badge>
        </div>
        <h3 className="mt-3 font-semibold leading-snug text-foreground">{item.title}</h3>
        <p className="mt-2 text-sm leading-relaxed text-muted">{item.content}</p>
      </CardBody>
    </Card>
  );
}

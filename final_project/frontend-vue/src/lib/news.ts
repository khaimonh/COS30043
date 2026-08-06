export type NewsItem = {
  id: number;
  date: string;
  title: string;
  content: string;
  category: string;
};

export const PAGE_SIZE = 6;

export function matchesSearch(item: NewsItem, query: string): boolean {
  const q = query.trim().toLowerCase();
  if (!q) return true;
  return (
    item.date.toLowerCase().includes(q) ||
    item.title.toLowerCase().includes(q) ||
    item.content.toLowerCase().includes(q) ||
    item.category.toLowerCase().includes(q)
  );
}

export function formatDate(date: string): string {
  const d = new Date(`${date}T00:00:00`);
  if (Number.isNaN(d.getTime())) return date;
  return d.toLocaleDateString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

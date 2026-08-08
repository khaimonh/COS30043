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

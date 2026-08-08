export function num(v: string | number | null | undefined): number | null {
  if (v === null || v === undefined || v === "") return null;
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}

export function fmtPrice(v: string | number | null | undefined): string {
  const n = num(v);
  if (n === null) return "—";
  return n.toLocaleString("vi-VN", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

export function fmtMoney(v: string | number | null | undefined): string {
  const n = num(v);
  if (n === null) return "—";
  return `${n.toLocaleString("vi-VN", { maximumFractionDigits: 0 })} ₫`;
}

export function fmtPct(v: string | number | null | undefined): string {
  const n = num(v);
  if (n === null) return "—";
  return `${n > 0 ? "+" : ""}${n.toFixed(2)}%`;
}

export function fmtQty(v: string | number | null | undefined): string {
  const n = num(v);
  if (n === null) return "—";
  return n.toLocaleString("vi-VN");
}

export function fmtDate(iso: string | null | undefined): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleDateString("en-GB", { day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit" });
}

export function fmtShortDate(iso: string | null | undefined): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
}

export function signed(n: string | number | null | undefined): string {
  const v = num(n);
  if (v === null) return "—";
  return `${v > 0 ? "+" : v < 0 ? "−" : ""}${Math.abs(v)}`;
}

export function dirClass(n: string | number | null | undefined, bright = false): string {
  const v = num(n);
  if (v === null || v === 0) return bright ? "text-band-muted" : "text-muted";
  const up = v > 0;
  if (bright) return up ? "text-up-bright" : "text-down-bright";
  return up ? "text-up" : "text-down";
}

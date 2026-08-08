import { ref, shallowReactive } from "vue";
import { BASE_URL } from "./api";
import type { Quote } from "./types";

const WS_URL = BASE_URL.replace(/^http/, "ws") + "/ws/quotes";

export const connected = ref(false);
const quotes = shallowReactive<Record<string, Quote | null>>({});

const subscribed = new Set<string>();
let ws: WebSocket | null = null;
let reconnectTimer: number | undefined;
let retries = 0;

function send(msg: unknown) {
  if (ws && ws.readyState === WebSocket.OPEN) ws.send(JSON.stringify(msg));
}

function connect() {
  ws = new WebSocket(WS_URL);
  ws.onopen = () => {
    connected.value = true;
    retries = 0;
    if (subscribed.size) send({ op: "subscribe", tickers: [...subscribed] });
  };
  ws.onmessage = (ev) => {
    let msg: any;
    try {
      msg = JSON.parse(ev.data);
    } catch {
      return;
    }
    if (msg.type === "snapshot" && msg.quotes) {
      for (const [tk, q] of Object.entries(msg.quotes)) {
        quotes[tk] = (q as Quote) ?? null;
      }
    } else if (msg.type === "tick" && msg.ticker) {
      const { type: _t, ticker: tk, ...rest } = msg;
      quotes[tk] = rest as Quote;
    }
  };
  ws.onclose = () => {
    connected.value = false;
    ws = null;
    clearTimeout(reconnectTimer);
    reconnectTimer = window.setTimeout(connect, Math.min(1000 * 2 ** retries, 15000));
    retries += 1;
  };
  ws.onerror = () => ws?.close();
}

export function subscribeTickers(tickers: string[]) {
  const fresh = tickers.filter((t) => t && !subscribed.has(t));
  tickers.forEach((t) => subscribed.add(t));
  if (!ws) connect();
  else if (connected.value && fresh.length) send({ op: "subscribe", tickers: fresh });
}

export function unsubscribeTickers(tickers: string[]) {
  tickers.forEach((t) => subscribed.delete(t));
  if (connected.value && tickers.length) send({ op: "unsubscribe", tickers });
}

export function quoteFor(ticker: string): Quote | null {
  return quotes[ticker] ?? null;
}

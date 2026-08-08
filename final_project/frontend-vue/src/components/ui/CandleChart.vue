<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from "vue";
import { createChart, CandlestickSeries, ColorType, type IChartApi, type Time } from "lightweight-charts";
import type { HistoryPoint } from "../../lib/types";

const props = defineProps<{ points: HistoryPoint[] }>();

const el = ref<HTMLDivElement | null>(null);
let chart: IChartApi | null = null;
let series: ReturnType<IChartApi["addSeries"]> | null = null;

type Candle = { time: Time; open: number; high: number; low: number; close: number };

function buildData(): Candle[] {
  return props.points
    .filter((p) => p.close !== null && p.close !== undefined && p.time)
    .map((p) => ({
      time: Math.floor(new Date(p.time as string).getTime() / 1000) as Time,
      open: Number(p.open) || 0,
      high: Number(p.high) || 0,
      low: Number(p.low) || 0,
      close: Number(p.close) || 0,
    }));
}

onMounted(() => {
  if (!el.value) return;
  chart = createChart(el.value, {
    autoSize: true,
    layout: {
      background: { type: ColorType.Solid, color: "transparent" },
      textColor: "#625245",
      fontFamily: "Martian Mono, ui-monospace, monospace",
      fontSize: 11,
    },
    grid: {
      vertLines: { color: "rgba(189,179,159,0.5)" },
      horzLines: { color: "rgba(189,179,159,0.5)" },
    },
    rightPriceScale: {
      borderColor: "#bdb39f",
      scaleMargins: { top: 0.12, bottom: 0.12 },
    },
    timeScale: {
      borderColor: "#bdb39f",
      timeVisible: true,
    },
    crosshair: {
      vertLine: { color: "rgba(28,34,84,0.6)", labelBackgroundColor: "#1c2254" },
      horzLine: { color: "rgba(28,34,84,0.6)", labelBackgroundColor: "#1c2254" },
    },
  });
  series = chart.addSeries(CandlestickSeries, {
    upColor: "#197037",
    downColor: "#a12f2f",
    borderUpColor: "#197037",
    borderDownColor: "#a12f2f",
    wickUpColor: "#197037",
    wickDownColor: "#a12f2f",
    priceLineColor: "#1c2254",
    priceLineStyle: 2,
  });
  const data = buildData();
  if (data.length) series.setData(data);
  chart.timeScale().fitContent();
});

watch(
  () => props.points,
  () => {
    if (!series || !chart) return;
    const data = buildData();
    if (!data.length) return;
    series.setData(data);
    chart.timeScale().fitContent();
  }
);
onBeforeUnmount(() => {
  chart?.remove();
  chart = null;
  series = null;
});
</script>

<template>
  <div ref="el" class="h-72 w-full sm:h-80" role="img" :aria-label="`${points.length} historical candles`" />
</template>

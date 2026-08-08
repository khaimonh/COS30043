<script setup lang="ts">
import { useI18n } from "../../i18n";
import Mark from "../ui/Mark.vue";

const { t, tf, lang } = useI18n();

const navLinks = [
  { href: "/", key: "nav.home" },
  { href: "/about", key: "nav.about" },
  { href: "/news", key: "nav.news" },
] as const;

const pressLinks = [
  { href: "/about", key: "footer.link.brief" },
  { href: "/news", key: "footer.link.daily" },
  { href: "/", key: "footer.link.figures" },
] as const;

const specs = [
  { key: "footer.spec.exchanges", value: "HOSE · HNX · UPCOM" },
  { key: "footer.spec.coverage", value: "500+ securities" },
  { key: "footer.spec.engine", value: "FIFO · RabbitMQ" },
  { key: "footer.spec.settlement", value: "VND · T+2" },
  { key: "footer.spec.calendar", value: "Mon–Fri · 09:00–15:00" },
] as const;

const quotes = [
  { sym: "VN-INDEX", chg: 0.42 },
  { sym: "VN30", chg: -0.18 },
  { sym: "HNX-INDEX", chg: 0.27 },
] as const;

const buildStamp = `FLX·${String(new Date().getFullYear())}·${lang.value.toUpperCase()}`;
const year = String(new Date().getFullYear());

function fmtChg(n: number): string {
  const sign = n >= 0 ? "+" : "−";
  return `${sign}${Math.abs(n).toFixed(2)}%`;
}
</script>

<template>
  <footer class="relative bg-paper">
    <div aria-hidden="true" class="mx-auto h-1 w-full max-w-6xl bg-rule" />

    <div class="mx-auto w-full max-w-6xl px-4 pt-16 pb-32 sm:px-6 sm:pt-20 sm:pb-40">
      <div class="grid gap-12 lg:grid-cols-12 lg:gap-10">
        <div class="lg:col-span-7">
          <p class="font-mono text-xs tracking-[0.25em] text-muted">
            {{ t("footer.kicker").toUpperCase() }}
          </p>
          <p
            class="mt-5 max-w-[18ch] text-[clamp(2.5rem,7vw,5rem)] font-display font-bold leading-[1.02] tracking-[-0.03em]"
          >
            {{ t("footer.statement") }}
          </p>
          <p class="mt-6 max-w-[56ch] text-base leading-relaxed text-muted">
            {{ t("footer.tagline") }}
          </p>
        </div>

        <aside class="lg:col-span-5">
          <div class="rounded-2xl border border-rule bg-paper-2 p-6">
            <div class="flex items-baseline justify-between gap-3">
              <p class="font-mono text-xs tracking-[0.25em] text-muted">
                {{ t("footer.specTitle").toUpperCase() }}
              </p>
              <p class="font-mono text-[10px] tracking-[0.2em] text-muted/70">
                {{ t("footer.demoNote") }}
              </p>
            </div>
            <dl class="mt-4 space-y-3 font-mono text-sm">
              <div
                v-for="row in specs"
                :key="row.key"
                class="flex items-baseline justify-between gap-4 border-b border-rule pb-3 last:border-0 last:pb-0"
              >
                <dt class="text-muted">{{ t(row.key) }}</dt>
                <dd class="text-right text-ink">{{ row.value }}</dd>
              </div>
            </dl>
          </div>
        </aside>
      </div>

      <div class="mt-14 grid gap-10 border-t border-rule pt-10 sm:grid-cols-2 lg:grid-cols-12 lg:gap-10">
        <div class="lg:col-span-4">
          <p class="font-mono text-xs tracking-[0.25em] text-muted">
            {{ t("footer.col.nav").toUpperCase() }}
          </p>
          <nav class="mt-4 flex flex-col gap-2" aria-label="Footer navigation">
            <RouterLink
              v-for="link in navLinks"
              :key="link.href"
              :to="link.href"
              class="font-mono text-sm text-ink transition-colors duration-150 hover:text-band"
            >
              {{ t(link.key) }}
            </RouterLink>
          </nav>
        </div>

        <div class="lg:col-span-4">
          <p class="font-mono text-xs tracking-[0.25em] text-muted">
            {{ t("footer.col.press").toUpperCase() }}
          </p>
          <ul class="mt-4 flex flex-col gap-2">
            <li v-for="link in pressLinks" :key="link.href">
              <RouterLink
                :to="link.href"
                class="font-mono text-sm text-ink transition-colors duration-150 hover:text-band"
              >
                {{ t(link.key) }}
              </RouterLink>
            </li>
          </ul>
          <p class="mt-5 font-mono text-xs leading-relaxed text-muted">
            {{ t("footer.contact") }}
            <a
              href="mailto:press@fluxus.local"
              class="ml-1 text-ink underline decoration-rule decoration-1 underline-offset-4 transition-colors duration-150 hover:decoration-band hover:text-band"
              >press@fluxus.local</a
            >
          </p>
        </div>

        <div class="lg:col-span-4">
          <p class="font-mono text-xs tracking-[0.25em] text-muted">
            {{ t("footer.col.market").toUpperCase() }}
          </p>
          <ul class="mt-4 flex flex-col gap-2 font-mono text-sm">
            <li
              v-for="q in quotes"
              :key="q.sym"
              class="flex items-baseline justify-between gap-3 border-b border-rule pb-2 last:border-0 last:pb-0"
            >
              <span class="text-ink">{{ q.sym }}</span>
              <span
                class="font-medium tabular-nums"
                :class="q.chg >= 0 ? 'text-up' : 'text-down'"
                >{{ fmtChg(q.chg) }}</span
              >
            </li>
          </ul>
          <p class="mt-4 font-mono text-[10px] leading-relaxed tracking-[0.05em] text-muted/70">
            {{ t("footer.disclaimer") }}
          </p>
        </div>
      </div>

      <div
        class="mt-12 flex flex-col gap-5 border-t border-rule pt-6 text-sm sm:flex-row sm:items-center sm:justify-between"
      >
        <span class="flex items-center gap-3">
          <Mark size="sm" />
          <span class="font-mono text-ink">{{ t("brand.name") }}</span>
          <span class="font-mono text-xs text-muted">{{ buildStamp }}</span>
        </span>
        <span class="font-mono text-xs text-muted">
          {{ tf("footer.rights", { year }) }}
        </span>
      </div>
    </div>
  </footer>
</template>

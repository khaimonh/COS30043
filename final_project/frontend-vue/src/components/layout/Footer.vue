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
  <footer class="position-relative bg-paper">
    <div aria-hidden="true" class="mx-auto h-1 w-100 max-w-6xl bg-rule" />

    <div class="mx-auto w-100 max-w-6xl px-3 py-4 px-sm-4 py-sm-4">
      <div class="row g-5">
        <div class="col-lg-7">
          <p class="font-mono text-xs tracking-[0.25em] text-muted">
            {{ t("footer.kicker").toUpperCase() }}
          </p>
          <p
            class="mt-2 max-w-[26ch] text-[clamp(1.5rem,2.75vw,2.25rem)] font-display fw-bold leading-[1.05] tracking-[-0.03em]"
          >
            {{ t("footer.statement") }}
          </p>
          <p class="mt-2 max-w-[56ch] text-base leading-relaxed text-muted">
            {{ t("footer.tagline") }}
          </p>
        </div>

        <aside class="col-lg-5">
          <div class="rounded-4 border border-rule bg-paper-2 p-3">
            <div class="d-flex align-items-baseline justify-content-between gap-3">
              <p class="font-mono text-xs tracking-[0.25em] text-muted">
                {{ t("footer.specTitle").toUpperCase() }}
              </p>
              <p class="font-mono text-[10px] tracking-[0.2em] text-muted/70">
                {{ t("footer.demoNote") }}
              </p>
            </div>
            <dl class="mt-2 space-y-2 font-mono text-sm">
              <div
                v-for="row in specs"
                :key="row.key"
                class="d-flex align-items-baseline justify-content-between gap-3 border-bottom border-rule pb-2 last:border-0 last:pb-0"
              >
                <dt class="text-muted">{{ t(row.key) }}</dt>
                <dd class="text-end text-ink">{{ row.value }}</dd>
              </div>
            </dl>
          </div>
        </aside>
      </div>

      <div class="mt-4 row g-5 border-top border-rule pt-4">
        <div class="col-12 col-lg-4">
          <p class="font-mono text-xs tracking-[0.25em] text-muted">
            {{ t("footer.col.nav").toUpperCase() }}
          </p>
          <nav class="mt-2 d-flex flex-column gap-1.5" aria-label="Footer navigation">
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

        <div class="col-12 col-lg-4">
          <p class="font-mono text-xs tracking-[0.25em] text-muted">
            {{ t("footer.col.press").toUpperCase() }}
          </p>
          <ul class="mt-2 d-flex flex-column gap-1.5">
            <li v-for="link in pressLinks" :key="link.href">
              <RouterLink
                :to="link.href"
                class="font-mono text-sm text-ink transition-colors duration-150 hover:text-band"
              >
                {{ t(link.key) }}
              </RouterLink>
            </li>
          </ul>
          <p class="mt-2 font-mono text-xs leading-relaxed text-muted">
            {{ t("footer.contact") }}
            <a
              href="mailto:press@fluxus.local"
              class="ms-1 text-ink underline decoration-rule decoration-1 underline-offset-4 transition-colors duration-150 hover:decoration-band hover:text-band"
              >press@fluxus.local</a
            >
          </p>
        </div>

        <div class="col-12 col-lg-4">
          <p class="font-mono text-xs tracking-[0.25em] text-muted">
            {{ t("footer.col.market").toUpperCase() }}
          </p>
          <ul class="mt-2 d-flex flex-column gap-1.5 font-mono text-sm">
            <li
              v-for="q in quotes"
              :key="q.sym"
              class="d-flex align-items-baseline justify-content-between gap-3 border-bottom border-rule pb-1.5 last:border-0 last:pb-0"
            >
              <span class="text-ink">{{ q.sym }}</span>
              <span
                class="fw-medium tabular-nums"
                :class="q.chg >= 0 ? 'text-up' : 'text-down'"
                >{{ fmtChg(q.chg) }}</span
              >
            </li>
          </ul>
          <p class="mt-2 font-mono text-[10px] leading-relaxed tracking-[0.05em] text-muted/70">
            {{ t("footer.disclaimer") }}
          </p>
        </div>
      </div>

      <div
        class="mt-4 d-flex flex-column gap-4 border-top border-rule pt-3 text-sm flex-sm-row align-items-sm-center justify-content-sm-between"
      >
        <span class="d-flex align-items-center gap-3">
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

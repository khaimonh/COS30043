<script setup lang="ts">
import { computed, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useI18n, type Lang } from "../../i18n";
import type { Dict } from "../../i18n/en";
import { quotes } from "../../lib/ticker";
import { token, user, isAdmin, logout } from "../../lib/session";

const { t, lang, setLang } = useI18n();
const route = useRoute();
const router = useRouter();
const open = ref(false);

type NavLink = { href: string; key: keyof Dict; auth?: boolean; admin?: boolean };

const allLinks: NavLink[] = [
  { href: "/", key: "nav.home" },
  { href: "/market", key: "nav.market" },
  { href: "/portfolio", key: "nav.portfolio", auth: true },
  { href: "/watchlist", key: "nav.watchlist", auth: true },
  { href: "/orders", key: "nav.orders", auth: true },
  { href: "/bank-accounts", key: "nav.bank", auth: true },
  { href: "/admin", key: "nav.admin", auth: true, admin: true },
  { href: "/news", key: "nav.news" },
  { href: "/about", key: "nav.about" },
];

const links = computed(() =>
  allLinks.filter(
    (l) => (!l.auth || token.value) && (!l.admin || isAdmin())
  )
);

const langs: Lang[] = ["en", "vi"];

const credits = [
  "FLUXUS · PRESSED DAILY",
  "NO.000500 · HOSE · HNX · UPCOM",
  "VND SETTLED · FIFO LOTS",
  "DEMO DATA · SAMPLE FEED",
];

function isActive(href: string): boolean {
  return href === "/" ? route.path === "/" : route.path.startsWith(href);
}

function signOut() {
  open.value = false;
  logout();
  router.replace("/");
}
</script>

<template>
  <header class="sticky-top z-3">
    <div class="border-top border-4 border-band bg-band text-band-ink shadow-float">
      <div class="mx-auto d-flex h-16 max-w-6xl align-items-center gap-3 px-3 px-sm-4">
        <div class="min-w-0 flex-grow-1 overflow-hidden" role="marquee" aria-label="Live quotes">
          <div class="ticker-marquee d-flex w-max align-items-center gap-5 whitespace-nowrap py-1 font-mono text-[13px]">
            <template v-for="dup in 2" :key="dup">
              <span v-for="q in quotes" :key="q.symbol + dup" class="d-flex align-items-baseline gap-2">
                <span class="fw-semibold tracking-wide">{{ q.symbol }}</span>
                <span class="text-band-ink">{{ q.price }}</span>
                <span :class="q.chg >= 0 ? 'text-up-bright' : 'text-down-bright'">
                  {{ q.chg >= 0 ? "+" : "−" }}{{ Math.abs(q.chg) }}
                </span>
              </span>
            </template>
          </div>
        </div>

        <nav class="d-none align-items-center gap-1 d-lg-flex" aria-label="Main">
          <RouterLink
            v-for="link in links"
            :key="link.href"
            :to="link.href"
            :class="[
              'rounded-pill px-3 py-1.5 font-mono text-sm tracking-wide transition-colors duration-150',
              isActive(link.href) ? 'bg-paper text-ink' : 'text-band-ink hover:bg-band-2',
            ]"
          >
            {{ t(link.key) }}
          </RouterLink>
        </nav>

        <div class="d-none align-items-center gap-2 d-lg-flex">
          <div v-if="user" class="d-none d-xl-block">
            <span class="max-w-[10rem] truncate font-mono text-xs text-band-muted">{{ user.full_name }}</span>
          </div>
          <button
            v-if="user"
            type="button"
            class="rounded-pill bg-transparent border border-band-ink/30 px-3 py-1 font-mono text-xs text-band-ink transition-colors duration-150 hover:bg-band-2"
            @click="signOut"
          >
            {{ t("nav.signOut") }}
          </button>
          <RouterLink
            v-else
            to="/login"
            class="rounded-pill bg-transparent border border-band-ink/30 px-3 py-1 font-mono text-xs text-band-ink transition-colors duration-150 hover:bg-band-2"
          >
            {{ t("nav.login") }}
          </RouterLink>
        </div>

        <div class="d-none align-items-center gap-0.5 rounded-pill border border-band-ink/30 p-0.5 d-lg-flex">
          <button
            v-for="l in langs"
            :key="l"
            type="button"
            :aria-pressed="lang === l"
            :class="[
              'rounded-pill px-3 py-1 font-mono text-xs transition-colors duration-150',
              lang === l ? 'bg-paper text-ink' : 'bg-transparent text-band-ink hover:text-paper',
            ]"
            @click="setLang(l)"
          >
            {{ l.toUpperCase() }}
          </button>
        </div>

        <div class="d-none h-10 overflow-hidden align-items-stretch gap-4 d-xxl-flex" aria-hidden="true">
          <span
            v-for="line in credits"
            :key="line"
            class="font-mono text-[10px] leading-[1.15] tracking-[0.3em] text-band-ink/75"
            style="writing-mode: vertical-rl"
          >
            {{ line }}
          </span>
        </div>

        <button
          type="button"
          class="d-flex bg-transparent h-9 w-9 align-items-center justify-content-center rounded-pill text-band-ink transition-colors duration-150 hover:bg-band-2 d-lg-none"
          :aria-expanded="open"
          aria-label="Toggle menu"
          @click="open = !open"
        >
          <svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <path v-if="open" d="M6 6l12 12M18 6L6 18" stroke-linecap="round" />
            <path v-else d="M4 7h16M4 12h16M4 17h16" stroke-linecap="round" />
          </svg>
        </button>
      </div>
    </div>

    <nav
      v-if="open"
      class="position-absolute top-100 start-4 end-4 rounded-top-3 border-4 border-bottom-0 border-band bg-paper p-3 shadow-float d-lg-none"
      aria-label="Mobile"
    >
      <div class="d-flex flex-column gap-1">
        <RouterLink
          v-for="link in links"
          :key="link.href"
          :to="link.href"
          class="rounded-pill px-3 py-2.5 font-mono text-sm tracking-wide"
          :class="isActive(link.href) ? 'bg-paper-2 fw-semibold text-ink' : 'text-muted'"
          @click="open = false"
        >
          {{ t(link.key) }}
        </RouterLink>
      </div>
      <div class="mt-3 d-flex flex-wrap align-items-center gap-2 border-top border-rule pt-3">
        <div class="d-flex align-items-center gap-0.5 rounded-pill border border-rule p-0.5">
          <button
            v-for="l in langs"
            :key="l"
            type="button"
            class="rounded-pill px-3 py-2 font-mono text-sm"
            :class="lang === l ? 'bg-band text-band-ink' : 'bg-transparent text-muted'"
            @click="setLang(l)"
          >
            {{ l.toUpperCase() }}
          </button>
        </div>
        <button
          v-if="user"
          type="button"
          class="rounded-pill border border-rule px-3 py-2 font-mono text-sm text-muted"
          @click="signOut"
        >
          {{ t("nav.signOut") }}
        </button>
        <RouterLink
          v-else
          to="/login"
          class="rounded-pill border border-rule px-3 py-2 font-mono text-sm text-muted"
          @click="open = false"
        >
          {{ t("nav.login") }}
        </RouterLink>
      </div>
    </nav>
  </header>
</template>

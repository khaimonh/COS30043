export const en = {
  "brand.name": "Fluxus",

  "nav.home": "Home",
  "nav.about": "About",
  "nav.news": "News",

  "home.badge": "Vietnam stock market, live",
  "home.title": "Trade Vietnam's market with confidence",
  "home.welcome":
    "Fluxus is a real-time trading playground for the Vietnamese stock exchange. Track live quotes, build watchlists, manage your portfolio and place orders — all in one calm, data-rich dashboard.",
  "home.ctaPrimary": "Explore the market",
  "home.ctaSecondary": "About Fluxus",
  "home.image1Alt": "Illustration of a rising candlestick chart",
  "home.image2Alt": "Preview of the Fluxus portfolio dashboard",
  "home.previewTitle": "A calm dashboard for active traders",
  "home.previewText":
    "Portfolio summaries, live quotes and order flow come together in one focused workspace — no clutter, no noise.",
  "home.feature1": "Live quotes",
  "home.feature1Text":
    "Prices are cached and refreshed on a poll cycle, then served as a single batched request.",
  "home.feature2": "Real order engine",
  "home.feature2Text":
    "Buy and sell orders run through a queue-backed execution engine with FIFO lot accounting.",
  "home.feature3": "Watchlists with targets",
  "home.feature3Text": "Track tickers and set target prices so the market comes to you.",

  "about.title": "About Fluxus",
  "about.paragraph":
    "Fluxus is a web application built to make Vietnam's stock market approachable. It pulls live prices, lets you build watchlists with target prices, and simulates a full portfolio lifecycle — deposits, holdings, and buy/sell orders backed by a real order engine. Designed for traders who want the numbers without the noise.",
  "about.formTitle": "Say hello",
  "about.firstNameLabel": "First name",
  "about.lastNameLabel": "Last name",
  "about.firstNamePlaceholder": "e.g. Minh",
  "about.lastNamePlaceholder": "e.g. Nguyen",
  "about.greetButton": "Greet me",
  "about.welcome": "Welcome, {name}!",
  "about.welcomeHint":
    "Type your name to get a greeting, then pick a scene to preview it below.",
  "about.sceneTitle": "Pick a scene",
  "about.mountain": "Mountain",
  "about.ocean": "Ocean",
  "about.mountainAlt": "Illustration of a mountain landscape",
  "about.oceanAlt": "Illustration of an ocean scene",

  "news.title": "Market news",
  "news.subtitle":
    "The latest headlines from Vietnam's financial markets.",
  "news.searchPlaceholder": "Search by date, title, content, or category…",
  "news.allCategories": "All categories",
  "news.results": "{n} items",
  "news.loading": "Loading news…",
  "news.empty": "No news matches your search.",
  "news.prev": "Prev",
  "news.next": "Next",
  "news.pageOf": "Page {page} of {total}",
} as const;

export type Dict = { [K in keyof typeof en]: string };

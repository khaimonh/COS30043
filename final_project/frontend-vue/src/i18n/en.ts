export const en = {
  "brand.name": "Fluxus",

  "nav.home": "Home",
  "nav.about": "About",
  "nav.news": "News",
  "nav.explore": "Explore",

  "footer.statement": "The market never sleeps. Neither should your edge.",
  "footer.rights": "© {year} Fluxus — Vietnam stock market playground",

  "home.heroTag": "HO CHI MINH · VIETNAM",
  "home.heroFigure": "500+",
  "home.title": "Trade Vietnam's market with confidence",
  "home.welcome":
    "Fluxus is a real-time trading playground for the Vietnamese stock exchange. Track live quotes, build watchlists, manage your portfolio and place orders — all in one calm, data-rich dashboard.",
  "home.ctaPrimary": "Explore the market",
  "home.ctaSecondary": "About Fluxus",
  "home.image1Alt": "Illustration of a rising candlestick chart",
  "home.image2Alt": "Preview of the Fluxus portfolio dashboard",

  "home.stat1Num": "3",
  "home.stat1Label": "exchanges",
  "home.stat2Num": "500+",
  "home.stat2Label": "securities",
  "home.stat3Num": "1",
  "home.stat3Label": "order engine",

  "home.specTitle": "What Fluxus does",
  "home.spec1Name": "Live quotes",
  "home.spec1Value": "Real-time",
  "home.spec1Note": "refreshed on a poll cycle, served as a single batched request",
  "home.spec2Name": "Order engine",
  "home.spec2Value": "FIFO lots",
  "home.spec2Note": "queue-backed execution with lot accounting",
  "home.spec3Name": "Watchlists",
  "home.spec3Value": "Target prices",
  "home.spec3Note": "alerts when your price is hit",
  "home.spec4Name": "Portfolio",
  "home.spec4Value": "End-to-end",
  "home.spec4Note": "deposits, holdings, and buy/sell orders",

  "home.ctaStripTitle": "The market is live right now.",
  "home.ctaStripNote": "Watch it, or trade it. Either way, it is in front of you.",

  "about.title": "About Fluxus",
  "about.salutation": "Hello,",
  "about.paragraph":
    "Fluxus is a web application built to make Vietnam's stock market approachable. It pulls live prices, lets you build watchlists with target prices, and simulates a full portfolio lifecycle — deposits, holdings, and buy/sell orders backed by a real order engine. Designed for traders who want the numbers without the noise.",
  "about.formTitle": "Say hello",
  "about.firstNameLabel": "First name",
  "about.lastNameLabel": "Last name",
  "about.firstNamePlaceholder": "e.g. Minh",
  "about.lastNamePlaceholder": "e.g. Nguyen",
  "about.greetButton": "Greet me",
  "about.ps": "p.s. your name becomes the welcome.",
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

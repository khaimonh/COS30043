export const en = {
  "brand.name": "Fluxus",

  "nav.home": "Home",
  "nav.about": "About",
  "nav.news": "News",

  "footer.statement": "One band to hold the market. The rest of the page stays yours.",
  "footer.rights": "© {year} Fluxus — pressed in Vietnam",

  "home.hero": "Vietnam's live market, pressed into one calm place.",
  "home.lede":
    "Fluxus streams real quotes from HOSE, HNX and UPCOM — over 500 securities — and runs a real order engine behind a portfolio you can actually trade. No noise between you and the numbers.",
  "home.liveQuote": "Live · {symbol} {price} ({chg})",
  "home.liveArrow": "{arrow} since close",

  "home.spec.title": "Spec sheet",
  "home.spec.demoNote": "Illustrative figures",
  "home.spec.origin": "Origin",
  "home.spec.liquidity": "Liquidity",
  "home.spec.sessions": "Sessions",
  "home.spec.feed": "Feed",
  "home.spec.est": "Est. build",

  "home.sector.title": "Sectors",
  "home.sector.statement":
    "One index, five thousand quiet voices — banks lead the print, realty and materials press on behind.",
  "home.sector.banks": "Banks",
  "home.sector.realty": "Realty",
  "home.sector.materials": "Materials",
  "home.sector.cons": "Consumer",

  "home.chart.caption": "VN-INDEX · daily",
  "home.chart.source": "Source: {source}",

  "home.credit.title": "In the sleeve",
  "home.credit.statement": "The band carries the numbers. The face holds the story.",
  "home.credit.memo": "Memo — the band's total width, set every session",
  "home.credit.positions": "Positions held on the sleeve",
  "home.credit.funds": "Credits in your account",
  "home.credit.orders": "FIFO lots, queued in order",

  "about.kicker": "The press",
  "about.title": "About Fluxus",
  "about.lede":
    "Fluxus is a web application that presses Vietnam's stock market into one calm surface: live prices, watchlists with target prices, and a full portfolio lifecycle — deposits, holdings, and buy/sell orders settled by a real FIFO engine.",
  "about.origin":
    "Founded in HCMC in 2001 as a boutique execution desk, Fluxus today is a market notebook — an empty face, and one band that streams every number that matters in printed credits.",
  "about.factsTitle": "Facts",
  "about.demoNote": "Illustrative figures",
  "about.fact.founded": "Founded",
  "about.fact.employees": "People",
  "about.fact.asset": "Assets",
  "about.fact.cto": "Press",

  "about.visitTitle": "Say hello",
  "about.firstNameLabel": "First name",
  "about.lastNameLabel": "Last name",
  "about.firstNamePlaceholder": "Minh",
  "about.lastNamePlaceholder": "Nguyen",
  "about.greetButton": "Greet me",
  "about.welcome": "Welcome, {name}!",
  "about.sceneTitle": "Pick a scene",
  "about.mountain": "Mountain",
  "about.ocean": "Ocean",
  "about.mountainAlt": "A mountain printed as sleeve art",
  "about.oceanAlt": "An ocean printed as sleeve art",

  "news.title": "Market news",
  "news.subtitle": "Headlines from Vietnam's exchanges, printed daily.",
  "news.demoNote": "Sample feed — swapped for the live endpoint in the full build.",
  "news.searchPlaceholder": "Search by date, title, content, or category…",
  "news.allCategories": "All categories",
  "news.results": "{n} items",
  "news.loading": "Setting the print…",
  "news.empty": "No news matches your search.",
  "news.prev": "Prev",
  "news.next": "Next",
  "news.pageOf": "Page {page} of {total}",
} as const;

export type Dict = { [K in keyof typeof en]: string };

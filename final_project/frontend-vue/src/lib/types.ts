export type Stock = {
  stock_id: string;
  ticker: string;
  company_name: string;
  exchange: string;
  sector: string;
  listing_date: string | null;
  listed: boolean;
};

export type Quote = {
  close_price?: string | number | null;
  open_price?: string | number | null;
  high_price?: string | number | null;
  low_price?: string | number | null;
  volume_accumulated?: string | number | null;
  change?: string | number | null;
  change_price?: string | number | null;
  pct_change?: string | number | null;
  price_change?: string | number | null;
  percent_change?: string | number | null;
  previous_price?: string | number | null;
  timestamp?: number | null;
  age_ms?: number | null;
  fallback?: string | null;
};

export type WatchlistEntry = {
  watchlist_id: string;
  stock_id: string;
  ticker: string;
  company_name: string;
  exchange: string;
  sector: string;
  target_price: string | null;
  current_price: string | null;
  created_at: string | null;
};

export type Portfolio = {
  portfolio_id: string;
  name: string;
  cash_balance: string;
};

export type Holding = {
  stock_id: string;
  ticker: string;
  company_name: string;
  quantity: number;
  lots: number;
  avg_cost: string;
  current_price: string | null;
  market_value: string | null;
  cost_basis: string;
  unrealized_pnl: string | null;
};

export type Summary = {
  portfolio_id: string;
  name: string;
  cash_balance: string;
  holdings_value: string;
  total_value: string;
  realized_pnl: string;
  allocations: {
    ticker: string;
    quantity: number;
    value: string;
    weight_pct: number;
    priced: boolean;
  }[];
};

export type ActivityEvent = {
  type: string;
  amount: string;
  ticker: string | null;
  quantity: number | null;
  price: string | null;
  created_at: string | null;
};

export type BankAccount = {
  bank_account_id: string;
  bank_name: string;
  account_number_masked: string;
  created_at?: string | null;
};

export type Order = {
  order_id: string;
  portfolio_id: string;
  stock_id: string;
  order_type: string;
  order_style: string;
  status: string;
  quantity: number;
  limit_price: string | null;
  created_at: string | null;
};

export type HistoryPoint = {
  time: string | null;
  open: string | null;
  high: string | null;
  low: string | null;
  close: string | null;
  volume: string | number | null;
};

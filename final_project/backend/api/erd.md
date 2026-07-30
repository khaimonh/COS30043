# Stock Trading Platform — ERD

## Entities

### ROLE
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| name | string | e.g. Admin, User |

### USER
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| role_id | FK -> ROLE.id | |
| username | string | |
| password_hash | string | hashed, never plaintext |
| email | string | |
| status | string | Active \| Suspended |
| created_at | timestamp | |

### PORTFOLIO
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| user_id | FK -> USER.id | max 3 per user (application-enforced, not a DB constraint) |
| name | string | |
| cash_balance | decimal | stored value, updated transactionally on every trade/cash txn |
| version | int | optimistic locking |

### BANK_ACCOUNT
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| user_id | FK -> USER.id | |
| account_number_encrypted | string | AES-256 encrypted, key stored outside the DB (KMS/secrets manager) |
| account_number_masked | string | e.g. "****1234", precomputed for UI display, decryption never needed to show this |
| bank_name | string | |
| created_at | timestamp | |

### CASH_TRANSACTION
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| portfolio_id | FK -> PORTFOLIO.id | |
| bank_account_id | FK -> BANK_ACCOUNT.id | |
| type | string | Deposit \| Withdrawal |
| amount | decimal | |
| created_at | timestamp | |

### STOCK
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| ticker | string | |
| company_name | string | |
| exchange | string | |
| sector | string | |
| — | — | prices NOT stored here; retrieved from external API + cached in Redis |

### PRICE_HISTORY
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| stock_id | FK -> STOCK.id | |
| price | decimal | |
| recorded_at | timestamp | |

### ORDER
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| portfolio_id | FK -> PORTFOLIO.id | |
| stock_id | FK -> STOCK.id | |
| order_type | string | Buy \| Sell |
| order_style | string | Market \| Limit |
| quantity | int | |
| limit_price | decimal | nullable — only set for Limit orders |
| status | string | Pending \| Filled \| Partially Filled \| Cancelled \| Rejected |
| created_at | timestamp | |

### TRADE
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| order_id | FK -> ORDER.id | one order can produce many trades (partial fills) |
| execution_price | decimal | |
| executed_quantity | int | |
| executed_at | timestamp | |

### HOLDING
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| portfolio_id | FK -> PORTFOLIO.id | |
| stock_id | FK -> STOCK.id | |
| purchase_price | decimal | |
| original_quantity | int | |
| remaining_quantity | int | reduced on sell, never merged with other lots |
| purchase_date | timestamp | |
| version | int | optimistic locking |

### HOLDING_ALLOCATION
Join entity between TRADE and HOLDING. Represents which holding lot(s) a sell trade consumed, and how much — needed because a single sell can span multiple purchase lots (FIFO).

| Field | Type | Notes |
|---|---|---|
| id | PK | |
| trade_id | FK -> TRADE.id | |
| holding_id | FK -> HOLDING.id | |
| quantity_consumed | int | |

### WATCHLIST
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| user_id | FK -> USER.id | |
| stock_id | FK -> STOCK.id | |
| target_price | decimal | nullable, optional price alert threshold |

---

## Relationships

```
ROLE               (1) ---- (N) USER
USER               (1) ---- (N) PORTFOLIO
USER               (1) ---- (N) BANK_ACCOUNT
USER               (1) ---- (N) WATCHLIST
PORTFOLIO          (1) ---- (N) HOLDING
PORTFOLIO          (1) ---- (N) ORDER
PORTFOLIO          (1) ---- (N) CASH_TRANSACTION
BANK_ACCOUNT       (1) ---- (N) CASH_TRANSACTION
STOCK              (1) ---- (N) HOLDING
STOCK              (1) ---- (N) ORDER
STOCK              (1) ---- (N) PRICE_HISTORY
STOCK              (1) ---- (N) WATCHLIST
ORDER              (1) ---- (N) TRADE
TRADE              (1) ---- (N) HOLDING_ALLOCATION
HOLDING            (1) ---- (N) HOLDING_ALLOCATION
```

`HOLDING_ALLOCATION` makes TRADE and HOLDING effectively many-to-many: one sell trade can consume across several holding lots, and one holding lot can be partially consumed by several sell trades over time.

## Key design notes

- **Concurrency**: `PORTFOLIO.version` and `HOLDING.version` back optimistic locking — every update checks and increments version to prevent lost updates under concurrent access.
- **Cash balance**: `PORTFOLIO.cash_balance` is a stored (not derived) column for low-latency reads. It must only ever be updated inside the same DB transaction as the triggering `TRADE` or `CASH_TRANSACTION` insert, to prevent drift.
- **No separate transaction history table**: transaction history is generated dynamically by combining `TRADE` and `CASH_TRANSACTION` records, avoiding duplicated data.
- **Bank account security**: raw account numbers are never stored in plaintext. `account_number_encrypted` is decrypted only server-side at the point of calling the payment gateway; `account_number_masked` is used for all UI display.
- **Stock prices**: `STOCK` holds only static metadata. Live prices come from an external API and are cached in Redis; `PRICE_HISTORY` stores historical snapshots for charting.

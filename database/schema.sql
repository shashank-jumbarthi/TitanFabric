CREATE TABLE IF NOT EXISTS fabrics (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    composition TEXT NOT NULL,
    finish TEXT NOT NULL,
    weight_gsm INTEGER NOT NULL,
    width_in INTEGER NOT NULL,
    min_yards INTEGER NOT NULL,
    price_per_yard REAL NOT NULL,
    lead_time_days INTEGER NOT NULL,
    sustainable INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS quote_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    email TEXT NOT NULL,
    destination TEXT NOT NULL CHECK (destination IN ('domestic', 'international')),
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS quote_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote_request_id INTEGER NOT NULL REFERENCES quote_requests(id),
    fabric_id TEXT NOT NULL REFERENCES fabrics(id),
    yards INTEGER NOT NULL CHECK (yards > 0)
);

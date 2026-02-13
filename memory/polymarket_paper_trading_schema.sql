-- Polymarket Paper Trading Database Schema
-- SQLite version

CREATE TABLE IF NOT EXISTS paper_trades (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  market_id TEXT,
  market_name TEXT,
  market_type TEXT,
  strategy TEXT,
  direction TEXT,
  entry_price DECIMAL,
  exit_price DECIMAL,
  quantity DECIMAL,
  pnl DECIMAL,
  exit_time TIMESTAMP,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS portfolio (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  total_value DECIMAL DEFAULT 100.00,
  cash DECIMAL DEFAULT 100.00,
  positions TEXT, -- JSON string
  trades_count INTEGER DEFAULT 0,
  win_count INTEGER DEFAULT 0,
  loss_count INTEGER DEFAULT 0,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS market_data (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  market_id TEXT,
  market_name TEXT,
  yes_price DECIMAL,
  no_price DECIMAL,
  volume DECIMAL,
  spread DECIMAL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Initialize portfolio
INSERT OR IGNORE INTO portfolio (id, total_value, cash, positions, trades_count, win_count, loss_count) 
VALUES (1, 100.00, 100.00, '{}', 0, 0, 0);

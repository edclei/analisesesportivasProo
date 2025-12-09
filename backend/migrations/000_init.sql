CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS accounts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT,
  type TEXT NOT NULL,
  user_id TEXT,
  balance NUMERIC DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS betslips (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT now(),
  bets JSONB,
  totalOdd NUMERIC,
  stake NUMERIC,
  potentialReturn NUMERIC,
  status TEXT,
  account_type TEXT,
  market_type TEXT
);

CREATE TABLE IF NOT EXISTS bet_justifications (
  id BIGSERIAL PRIMARY KEY,
  betslip_id BIGINT,
  summary TEXT,
  meta JSONB,
  created_at TIMESTAMPTZ DEFAULT now(),
  expire_at TIMESTAMPTZ DEFAULT (now() + interval '24 hours')
);

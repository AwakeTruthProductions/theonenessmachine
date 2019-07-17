CREATE TABLE IF NOT EXISTS quote (
  quote_id integer PRIMARY KEY,
  quote text NOT NULL,
  author text NOT NULL,
  created_date text NOT NULL,
  UNIQUE(quote, author)
)
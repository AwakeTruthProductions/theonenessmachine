INSERT OR IGNORE INTO quote (
  quote,
  author,
  created_date
) VALUES (
  :quote,
  :author,
  datetime()
)

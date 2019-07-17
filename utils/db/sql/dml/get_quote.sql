SELECT
  q.quote_id,
  q.quote,
  q.author
FROM quote q
WHERE NOT EXISTS (
  SELECT qi.quote_id FROM quoted_imaged qi
  WHERE qi.quote_id = q.quote_id
)
LIMIT 1

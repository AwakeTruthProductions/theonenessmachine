SELECT
  q.quote_id,
  q.quote,
  q.author
FROM quote q
WHERE NOT EXISTS (
  SELECT qi.quote_id FROM quoted_image qi
  WHERE qi.quote_id = q.quote_id
)
AND q.author in (
	'Ramana Maharshi', 'Eckhart Tolle', 'Sri Nisargadatta Maharaj',
	'Byron Katie', 'Sathya Sai Baba', 'Adyashanti', 'Mooji', 'Meister Eckhart',
	'H. W. L. Poonja', 'Gangaji', 'Gautama Buddha'
)
AND length(q.quote) < 300
LIMIT 1000

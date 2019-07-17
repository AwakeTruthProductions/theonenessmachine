INSERT INTO quoted_image (
  source_id,
  disk_path,
  quote_id,
  created_date
) VALUES (
  :source_id,
  :disk_path,
  :quote_id,
  datetime()
)

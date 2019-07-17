CREATE TABLE IF NOT EXISTS quoted_image (
  quoted_image_id integer PRIMARY KEY,
  source_id text NOT NULL,
  disk_path text NOT NULL,
  quote_id text NOT NULL,
  created_date text NOT NULL,
  FOREIGN KEY (quote_id) REFERENCES quote (quote_id)
)
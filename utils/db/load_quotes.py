from utils.db import db
import csv
import sys


def add_quotes_from_file(file_path):
    conn = db.create_connection()
    sql = open('utils/data/sql/dml/insert_quote.sql').read()
    quote_file = open(file_path)
    file_reader = csv.reader(quote_file)

    # csv rows: author, quote
    with conn:
        for row in file_reader:
            db.execute_sql(conn, sql, {'quote': row[1], 'author': row[0]})


if __name__ == "__main__":
    if len(sys.argv) > 1:
        add_quotes_from_file(sys.argv[1])

from utils.db import db
import csv
import sys


def create_database():
    conn = db.create_connection('database/oneness_machine.db')
    quote_sql = open('utils/data/sql/ddl/quote.sql').read()
    quoted_image_sql = open('utils/data/sql/ddl/quoted_image.sql').read()
    with conn:
        db.execute_sql(conn, quote_sql)
        db.execute_sql(conn, quoted_image_sql)


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
    create_database()
    if len(sys.argv) > 1:
        add_quotes_from_file(sys.argv[1])

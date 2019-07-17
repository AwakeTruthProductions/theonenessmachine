import textwrap
from utils.db import db


def wrap_text_by_width(drawer, text, font, max_width):
    split_count = 0
    split_text = text
    need_split = True

    while need_split:
        text_width = drawer.textsize(split_text, font)[0]
        if text_width > max_width:
            split_count += 1
            text_length = len(split_text)
            split_text = split_text[:round(text_length/2)]
        else:
            need_split = False

    fulltext_length = len(text)
    true_text_width = fulltext_length/(split_count*2) \
        if split_count*2 != 0 else max_width
    split_text_arr = textwrap.wrap(text, true_text_width)
    new_line_text_arr = ['{0}\n'.format(el) for el in split_text_arr]
    split_text = ''.join(new_line_text_arr)
    return split_text


def insert_quoted_image(source_id, disk_path, quote_id):
    params = {
        'source_id': source_id,
        'disk_path': disk_path,
        'quote_id': quote_id
    }
    conn = db.create_connection()
    sql = open('utils/db/sql/dml/insert_quoted_image.sql').read()
    with conn:
        db.execute_sql(conn, sql, params)

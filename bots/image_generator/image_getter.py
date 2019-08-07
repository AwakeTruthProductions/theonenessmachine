import logging
import random
import requests
import uuid
from utils.aws import ssm
from utils.db import db

logger = logging.getLogger()

GET_QUOTE_SQL_PATH = 'utils/db/sql/dml/get_quote.sql'
GET_USED_IMAGE_SQL_PATH = 'utils/db/sql/dml/get_used_images.sql'


def get_image_details(category='nature'):
    pixaby_key = ssm.get_secure_parameter('oneness-machine-pixaby-access')
    url = 'https://pixabay.com/api'
    params = {
        'key': pixaby_key, 'q': 'nature+peace',
        'image_type': 'photo', 'orientation': 'horizontal',
        'category': category, 'min_width': 1280, 'min_height': 719,
        'safesearch': True, 'per_page': 200
    }
    pixaby = requests.get(url, params)
    if pixaby.status_code == 200:
        res = pixaby.json()
        if res['hits']:
            image_url, source_id = get_unused_image_url(res['hits'], 'pixaby')
            quote_id, quote, author = get_unused_quote()
            get_picture = requests.get(image_url)
            if get_picture.status_code == 200:
                image_path = f'assets/images/{source_id}{uuid.uuid4().hex}.png'
                with open(image_path, 'wb') as f:
                    f.write(get_picture.content)

                return {
                    'image_path': image_path, 'quote': quote,
                    'author': author, 'quote_id': quote_id,
                    'source_id': source_id
                }
        else:
            return {}


def get_unused_image_url(image_hits, source):
    conn = db.create_connection()
    old_images = []
    with conn:
        old_images = get_used_image_list(conn)
        old_image_list = [item for sublist in old_images for item in sublist]
        for hit in image_hits:
            source_id = f'{source}_{str(hit["id"])}'
            if source_id not in old_image_list and hit['largeImageURL']:
                return (hit['largeImageURL'], source_id)

    return ()


def get_unused_quote():
    conn = db.create_connection()
    sql = open(GET_QUOTE_SQL_PATH).read()
    with conn:
        new_quote = random.choice(db.execute_sql(conn, sql, {}, True))
        if new_quote:
            return (
                new_quote[0],
                new_quote[1],
                new_quote[2]
            )
    return None


def get_used_image_list(conn):
    sql = open(GET_USED_IMAGE_SQL_PATH).read()
    with conn:
        used_images = db.execute_sql(conn, sql, {}, True)
        return used_images

    return []

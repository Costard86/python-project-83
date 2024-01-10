import datetime as dt
import contextlib

import psycopg2
from psycopg2.extras import NamedTupleCursor


SELECT_URL_BY_NAME = 'SELECT * FROM urls WHERE urls.name = %s;'
SELECT_URL_BY_ID = 'SELECT * FROM urls WHERE urls.id = %s;'

SELECT_URLS = """
SELECT
  DISTINCT ON (urls.id)
    urls.id,
    urls.name,
    urls.created_at
FROM urls
ORDER BY
    urls.id;
"""

INSERT_URL = """
INSERT INTO urls (name, created_at)
VALUES (%s, %s)
RETURNING id;
"""


@contextlib.contextmanager
def connection(db_url):
    conn = psycopg2.connect(db_url)
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    else:
        conn.commit()
    finally:
        conn.close()


def get_url_by_name(conn, name):
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(SELECT_URL_BY_NAME, (name,))
        found_item = curs.fetchone()
    return found_item


def get_url_by_id(conn, id):
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(SELECT_URL_BY_ID, (id,))
        found_item = curs.fetchone()
    return found_item


def get_urls(conn):
    with conn.cursor() as curs:
        curs.execute(SELECT_URLS)
        all_entries = curs.fetchall()
    return all_entries


def add_to_urls(conn, url):
    with conn.cursor() as curs:
        curs.execute(INSERT_URL, (url, dt.datetime.now()))
        returned_id, = curs.fetchone()
    return returned_id




import logging as logger
import sqlite3

logger.basicConfig(format='%(asctime)s - %(message)s', level=logger.INFO)


def create_connection(db_file = 'database/oneness_machine.db'):
    """ creates a SQLlite db connection to the db_file provided
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file, isolation_level=None)
        return conn
    except sqlite3.Error as err:
        logger.error(err)

    return None

def execute_sql(conn, sql, params={}, fetch=False):
    """ executes the sql provided
    :param conn: connection object
    :param sql: sql string
    :param params: sql parameters tuple or dict
        (depending on parameterization style)
    :param fetch: bool indicating whether to fetch rows
    :return: None or rows based on fetch arg
    """
    try:
        c = conn.cursor()
        c.execute(sql, params)
        if fetch:
            return c.fetchall()
        else:
            return None
    except sqlite3.Error as err:
        logger.error(err)

    return None
from utils import DISCARD_TAGS
from config import DATABASE_URL

def insert_data_point(conn, reading):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO readings (time, value, tags) VALUES (%s, %s, %s) "
            "ON CONFLICT (time, tags) DO NOTHING",
            reading,
        )
    conn.commit()

def normal_user_data_read(conn, start_time=None, end_time=None):
    query = (
        "SELECT time, value, tags FROM readings "
        "WHERE time > now() - interval '1 hour' "
        "AND NOT (tags && %s)"
    )
    params = [list(DISCARD_TAGS)]

    if start_time is not None:
        query += " AND time >= %s"
        params.append(start_time)
    if end_time is not None:
        query += " AND time <= %s"
        params.append(end_time)

    with conn.cursor() as cur:
        cur.execute(query, params)
        return cur.fetchall()


def admin_user_data_read(conn, start_time=None, end_time=None):
    conditions = []
    params = []

    if start_time is not None:
        conditions.append("time >= %s")
        params.append(start_time)
    if end_time is not None:
        conditions.append("time <= %s")
        params.append(end_time)

    query = "SELECT time, value, tags FROM readings"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    with conn.cursor() as cur:
        cur.execute(query, params)
        return cur.fetchall()
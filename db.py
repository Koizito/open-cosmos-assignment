from utils import DISCARD_TAGS

DATABASE_URL = "postgresql://app:app@localhost:5432/app"

def insert_data_point(conn, reading):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO readings (time, value, tags) VALUES (%s, %s, %s)",
            reading,
        )
    conn.commit()

def normal_user_data_read(conn):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT time, value, tags FROM readings "
            "WHERE time > now() - interval '1 hour' "
            "AND NOT (tags && %s)",
            (list(DISCARD_TAGS),),
        )
        return cur.fetchall()

def admin_user_data_read(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT time, value, tags FROM readings")
        return cur.fetchall()
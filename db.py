import psycopg

DATABASE_URL = "postgresql://app:app@localhost:5432/app"

def insert_readings(readings):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO readings (time, value, tags) VALUES (%s, %s, %s)",
                readings,
            )
        conn.commit()
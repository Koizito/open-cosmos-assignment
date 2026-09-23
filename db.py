def insert_reading(conn, reading):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO readings (time, value, tags) VALUES (%s, %s, %s)",
            reading,
        )
    conn.commit()
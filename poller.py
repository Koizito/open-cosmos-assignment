import struct
import time
from datetime import datetime, timezone

import requests
import psycopg

from db import insert_data_point
from config import POLLER_URL, POLLER_INTERVAL, DATABASE_URL

def parse(item):
    value = struct.unpack("<f", bytes(item["value"]))[0]
    timestamp = datetime.fromtimestamp(item["time"], tz=timezone.utc)
    return (timestamp, value, item["tags"])

def run():
    conn = psycopg.connect(DATABASE_URL)
    try:
        while True:
            try:
                response = requests.get(POLLER_URL, timeout=5)
                response.raise_for_status()
                insert_data_point(conn, parse(response.json()))
            except requests.RequestException:
                pass
            except psycopg.OperationalError:
                conn.close()
                conn = psycopg.connect(DATABASE_URL)
            time.sleep(POLLER_INTERVAL)
    finally:
        conn.close()

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        pass
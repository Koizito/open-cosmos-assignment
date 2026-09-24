import time
import struct
from datetime import datetime, timezone

import requests
import psycopg

from db import DATABASE_URL, insert_data_point

URL = "http://localhost:28462/"
INTERVAL = 1

def run(stop_event):
    conn = psycopg.connect(DATABASE_URL)
    try:
        while not stop_event.is_set():
            try:
                response = requests.get(URL)
                json_response = response.json()

                value = struct.unpack("<f", bytes(json_response["value"]))[0]
                timestamp = datetime.fromtimestamp(
                    json_response["time"], tz=timezone.utc
                )

                insert_data_point(conn, (timestamp, value, json_response["tags"]))
            except requests.RequestException:
                pass
            stop_event.wait(INTERVAL)
    finally:
        conn.close()
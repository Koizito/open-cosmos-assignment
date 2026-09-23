import time
import requests
import struct
from db import insert_reading
import psycopg
from datetime import datetime, timezone

DATABASE_URL = "postgresql://app:app@localhost:5432/app"
URL = "http://localhost:28462/"
INTERVAL = 1

def main():
    conn = psycopg.connect(DATABASE_URL)
    while True:
        try:
            response = requests.get(URL)
            json_response = response.json()
            print(json_response["time"])
            print(json_response["tags"])
            print(json_response["value"])
            print(struct.unpack('<f', bytes(json_response["value"]))[0])

            value = struct.unpack("<f", bytes(json_response["value"]))[0]
            timestamp = ts = datetime.fromtimestamp(json_response["time"], tz=timezone.utc)

            insert_reading(conn, (timestamp, value, json_response["tags"]))
        except requests.RequestException:
            pass
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()

import time
import requests
import struct

URL = "http://localhost:28462/"
INTERVAL = 0.01

def main():
    while True:
        try:
            response = requests.get(URL)
            json_response = response.json()
            print(json_response["time"])
            print(json_response["tags"])
            print(json_response["value"])
            print(struct.unpack('<f', bytes(json_response["value"]))[0])
        except requests.RequestException:
            pass
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
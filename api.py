import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException
from psycopg_pool import ConnectionPool

import poller
from db import DATABASE_URL, admin_user_data_read, normal_user_data_read
from utils import discard_reasons

pool = ConnectionPool(DATABASE_URL, min_size=1, max_size=10)

@asynccontextmanager
async def lifespan(app):
    stop_event = threading.Event()
    thread = threading.Thread(target=poller.run, args=(stop_event,), daemon=True)
    thread.start()
    yield
    stop_event.set()
    thread.join(timeout=5)

app = FastAPI(lifespan=lifespan)

@app.get("/readings")
def list_readings():
    with pool.connection() as conn:
        rows = normal_user_data_read(conn)
    return [
        {"time": time.isoformat(), "value": value, "tags": tags}
        for time, value, tags in rows
    ]

@app.get("/admin/readings")
def list_all_readings():
    with pool.connection() as conn:
        rows = admin_user_data_read(conn)
    return [
        {
            "time": time.isoformat(),
            "value": value,
            "tags": tags,
            "discard_reasons": discard_reasons(time, tags),
        }
        for time, value, tags in rows
    ]
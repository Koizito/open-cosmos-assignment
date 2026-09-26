import threading
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Header, HTTPException
from psycopg_pool import ConnectionPool

import poller
from db import DATABASE_URL, admin_user_data_read, normal_user_data_read
from utils import discard_reasons
from config import ADMIN_TOKEN

pool = ConnectionPool(DATABASE_URL, min_size=1, max_size=10, open=True)

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
def list_readings(
    start_time: datetime | None = None,
    end_time: datetime | None = None,
):
    with pool.connection() as conn:
        rows = normal_user_data_read(conn, start_time, end_time)
    return [
        {"time": t.isoformat(), "value": v, "tags": tags}
        for t, v, tags in rows
    ]

@app.get("/admin/readings")
def list_all_readings(
    x_admin_token: str = Header(...),
    start_time: datetime | None = None,
    end_time: datetime | None = None,
):
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="invalid admin token")
    with pool.connection() as conn:
        rows = admin_user_data_read(conn, start_time, end_time)
    return [
        {
            "time": t.isoformat(),
            "value": v,
            "tags": tags,
            "discard_reasons": discard_reasons(t, tags),
        }
        for t, v, tags in rows
    ]
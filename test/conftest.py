import psycopg
import pytest
from fastapi.testclient import TestClient

import api
from db import DATABASE_URL


@pytest.fixture
def conn():
    c = psycopg.connect(DATABASE_URL)
    with c.cursor() as cur:
        cur.execute("DELETE FROM readings")
    c.commit()
    yield c
    c.close()


@pytest.fixture
def client():
    return TestClient(api.app)


@pytest.fixture
def insert(conn):
    def _insert(time, value, tags):
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO readings (time, value, tags) VALUES (%s, %s, %s)",
                (time, value, tags),
            )
        conn.commit()
    return _insert
from datetime import datetime, timedelta, timezone


def now():
    return datetime.now(timezone.utc)


def test_normal_user_sees_recent_untagged(insert, client):
    insert(now(), 0.5, [])
    r = client.get("/readings")
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_normal_user_hides_old_rows(insert, client):
    insert(now() - timedelta(hours=2), 0.5, [])
    assert client.get("/readings").json() == []


def test_normal_user_hides_tagged_rows(insert, client):
    insert(now(), 0.5, ["system"])
    assert client.get("/readings").json() == []


def test_normal_user_time_filter_upper_bound(insert, client):
    insert(now(), 0.5, [])
    past = (now() - timedelta(minutes=1)).isoformat().replace("+00:00", "Z")
    r = client.get("/readings", params={"end_time": past})
    assert r.json() == []


def test_normal_user_time_filter_lower_bound(insert, client):
    insert(now(), 0.5, [])
    past = (now() - timedelta(minutes=1)).isoformat().replace("+00:00", "Z")
    assert len(client.get(f"/readings?start_time={past}").json()) == 1


def test_admin_sees_old_row_with_reason(insert, client):
    insert(now() - timedelta(hours=2), 0.5, [])
    body = client.get("/admin/readings").json()
    assert len(body) == 1
    assert body[0]["discard_reasons"] == ["too old"]


def test_admin_sees_tagged_row_with_reason(insert, client):
    insert(now(), 0.5, ["suspect"])
    body = client.get("/admin/readings").json()
    assert body[0]["discard_reasons"] == ["tagged suspect"]


def test_admin_and_normal_user_disagree(insert, client):
    insert(now(), 0.5, [])
    insert(now(), 0.6, ["system"])
    assert len(client.get("/readings").json()) == 1
    assert len(client.get("/admin/readings").json()) == 2
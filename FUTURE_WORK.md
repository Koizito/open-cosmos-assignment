# Future Work

What I'd do with more time, roughly in the order I'd tackle it.

## Logging

There's no logging at all right now. The poller catches `requests.RequestException` and discards it, so if the mock server goes down, nothing tells you. You just notice no new rows arriving. Same for the reconnect path, which is silent. I could use Python's `logging` module, which would cover the basics without adding a dependency.

## The poller can die quietly

Right now the poller catches `OperationalError`, tries to reconnect once, and if that fails the process dies. That's neither a proper retry loop nor a deliberate "let it crash", it's just a single attempt that works as a placeholder for an actual strategy. If the DB is down for more than a moment, the poller exits. Under a supervisor it gets restarted, but each restart is a gap in the data, and a sustained outage turns into a crash loop. I'd either retry with backoff in-process or commit to crashing and let a supervisor handle it.

## Pagination

Both endpoints return everything that matches the filter. For this assignment it's fine, but it becomes a problem with larger volumes of data. The admin query with no time filter would try to materialize the whole table. The admin endpoint is the priority since the user endpoint is already bounded by the one-hour age filter.

## Real auth

The admin endpoint takes a shared secret in a header. It proves the boundary exists, but this isn't real authentication. There is no user identity, no roles, no way to revoke one person's access without rotating the token for everyone. A real version would have a user table or an external identity provider, session tokens, and a role check on the route.

## TimescaleDB

The data is a time series, and PostgreSQL handles it fine at this volume. At hundreds of millions of points I'd move to TimescaleDB. This is a PostgreSQL extension, so the SQL barely changes, but it partitions by time automatically. Queries only scan the chunks they need, old data is dropped by dropping a chunk instead of `DELETE` plus vacuum, and historical data gets columnar compression. The cost is operational: tuning chunk sizes, managing the extension, losing portability to plain PostgreSQL.

## A separate test database

The tests run against the dev database and `DELETE FROM readings` before each one, which wipes local data. The fix is a `TEST_DATABASE_URL` pointing at a second database. Do keep in mind, this isn't the same as mocking. The tests hit a real PostgreSQL Database on purpose, and that's what caught the `IndeterminateDatatype` bug. Mocking would have hidden it.

## Configurable discard rules

The rules (one hour, the tags `system` and `suspect`) are constants in `utils.py`. If admins needed to change them at runtime, they'd move to a config table. This doesn't require storing the discard reason per row. The reason stays derived, only its inputs become dynamic.
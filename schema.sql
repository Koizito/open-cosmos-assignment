CREATE TABLE IF NOT EXISTS readings (
    time   timestamptz NOT NULL,
    value  real NOT NULL,
    tags   text[] NOT NULL DEFAULT '{}',
    PRIMARY KEY (time, tags)
);
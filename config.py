import os

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://app:app@localhost:5432/app")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "secret")
POLLER_URL = os.environ.get("POLLER_URL", "http://localhost:28462/")
POLLER_INTERVAL = float(os.environ.get("POLLER_INTERVAL", "1"))

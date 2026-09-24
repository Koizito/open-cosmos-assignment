from datetime import datetime, timedelta, timezone

DISCARD_TAGS = {"system", "suspect"}
MAX_AGE = timedelta(hours=1)

def discard_reasons(time, tags):
    reasons = []
    if time <= datetime.now(timezone.utc) - MAX_AGE:
        reasons.append("too old")
    for tag in set(tags) & DISCARD_TAGS:
        reasons.append(f"tagged {tag}")
    return reasons
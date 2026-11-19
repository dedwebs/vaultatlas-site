#!/usr/bin/env python3
"""Validate feed/now-live.json against its schema plus cross-field rules.

Usage: python3 scripts/validate_feed.py [feed.json] [schema.json]
Needs: pip install jsonschema
"""
import json
import sys
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from jsonschema import Draft202012Validator

feed_path = sys.argv[1] if len(sys.argv) > 1 else "feed/now-live.json"
schema_path = sys.argv[2] if len(sys.argv) > 2 else "feed/now-live.schema.json"
EASTERN = ZoneInfo("America/New_York")


def parse(raw):
    if len(raw) == 10:  # YYYY-MM-DD, Eastern midnight (matches the app)
        return datetime.fromisoformat(raw).replace(tzinfo=EASTERN)
    return datetime.fromisoformat(raw.replace("Z", "+00:00"))


with open(feed_path, encoding="utf-8") as f:
    feed = json.load(f)
with open(schema_path, encoding="utf-8") as f:
    schema = json.load(f)

errors = [
    f"schema: {'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}"
    for e in Draft202012Validator(schema).iter_errors(feed)
]

if not errors:
    try:
        now = datetime.now(timezone.utc)
        if parse(feed["updatedAt"]) > now + timedelta(days=1):
            errors.append("updatedAt is more than one day in the future")

        ids = [e["id"] for e in feed["events"]]
        for dup in sorted({i for i in ids if ids.count(i) > 1}):
            errors.append(f"duplicate event id: {dup}")
        for e in feed["events"]:
            if parse(e["end"]) <= parse(e["start"]):
                errors.append(f"event {e['id']}: end must be after start")

        s = feed["season"]
        if s.get("start") and s.get("endEstimate") and parse(s["endEstimate"]) <= parse(s["start"]):
            errors.append("season: endEstimate must be after start")

        n = feed["nukeCodes"]
        codes = [n["alpha"], n["bravo"], n["charlie"]]
        if not (all(len(c) == 8 and c.isdigit() for c in codes) or not any(codes)):
            errors.append("nukeCodes: alpha/bravo/charlie must all be 8 digits or all empty")
        if n.get("validFrom") and n.get("validTo") and parse(n["validTo"]) <= parse(n["validFrom"]):
            errors.append("nukeCodes: validTo must be after validFrom")
    except ValueError as exc:
        errors.append(f"date parse error: {exc}")

if errors:
    print(f"{feed_path}: INVALID")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print(f"{feed_path}: OK ({len(feed['events'])} events)")

#!/usr/bin/env python3
"""
Κατεβάζει φρέσκα TLE sets από το space-track.org και τα γράφει σε data/tle_data.json.
Σχεδιασμένο να τρέχει είτε τοπικά είτε μέσα από το GitHub Action
(.github/workflows/update-tle.yml) αυτού του repo.

Διαπιστευτήρια μέσω environment variables (ΠΟΤΕ hardcoded):
    SPACETRACK_USER, SPACETRACK_PASS

Χρήση:
    python3 spacetrack_fetch.py                 # προεπιλεγμένοι δορυφόροι
    python3 spacetrack_fetch.py 25544 41747 67899
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

LOGIN_URL = "https://www.space-track.org/ajaxauth/login"
QUERY_URL = (
    "https://www.space-track.org/basicspacedata/query/class/gp/"
    "NORAD_CAT_ID/{norad_ids}/orderby/EPOCH%20desc/format/json"
)
DEFAULT_NORAD_IDS = [25544, 41747, 67899]  # ISS, Intelsat 36, Starlink-36878
OUTPUT_PATH = Path(__file__).parent / "data" / "tle_data.json"


def fetch_tles(norad_ids):
    user = os.environ.get("SPACETRACK_USER")
    pwd = os.environ.get("SPACETRACK_PASS")
    if not user or not pwd:
        sys.exit("Λείπουν τα SPACETRACK_USER / SPACETRACK_PASS.")

    session = requests.Session()
    resp = session.post(LOGIN_URL, data={"identity": user, "password": pwd}, timeout=20)
    resp.raise_for_status()
    if "fail" in resp.text.lower() and len(resp.text) < 200:
        sys.exit(f"Αποτυχία login: {resp.text}")

    url = QUERY_URL.format(norad_ids=",".join(str(i) for i in norad_ids))
    data_resp = session.get(url, timeout=30)
    data_resp.raise_for_status()

    out = []
    for rec in data_resp.json():
        out.append({
            "id": rec.get("NORAD_CAT_ID"),
            "name": rec.get("OBJECT_NAME", "").strip(),
            "line1": rec.get("TLE_LINE1"),
            "line2": rec.get("TLE_LINE2"),
            "epoch": rec.get("EPOCH"),
        })
    return out


def main():
    norad_ids = [int(a) for a in sys.argv[1:]] or DEFAULT_NORAD_IDS
    tles = fetch_tles(norad_ids)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {"fetched_at": datetime.now(timezone.utc).isoformat(), "satellites": tles}
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Γράφτηκαν {len(tles)} TLE sets στο {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

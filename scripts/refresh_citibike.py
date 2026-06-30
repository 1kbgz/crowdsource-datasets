#!/usr/bin/env python3
"""Refresh bikeshare/citibike/stations.csv from the Citi Bike GBFS feed.

The owned index of Citi Bike (NYC) docking stations — the keys participants
predict bike availability for. Source: the public GBFS `station_information`
feed (no key). Columns: station_id, name, lat, lon, capacity — sorted by
station_id for stable diffs. `station_id` is the index key (it matches the
`station_status` feed used at resolution).
"""
import csv
import io
import os

import requests

URL = "https://gbfs.citibikenyc.com/gbfs/en/station_information.json"
COLS = ["station_id", "name", "lat", "lon", "capacity"]
OUT = os.path.join(os.path.dirname(__file__), "..", "bikeshare", "citibike", "stations.csv")


def main() -> None:
    resp = requests.get(URL, headers={"User-Agent": "crowdsource-datasets/1.0 (+https://crowdsource.sh)"}, timeout=30)
    resp.raise_for_status()
    stations = resp.json()["data"]["stations"]
    rows = []
    for s in stations:
        if not s.get("station_id"):
            continue
        rows.append({c: s.get(c, "") for c in COLS})
    rows.sort(key=lambda r: str(r["station_id"]))
    if len(rows) < 100:
        raise SystemExit(f"refusing to write only {len(rows)} stations (feed likely broke)")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLS, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    with open(OUT, "w") as f:
        f.write(buf.getvalue())
    print(f"wrote {len(rows)} stations to {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()

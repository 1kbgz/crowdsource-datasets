# crowdsource-datasets

Owned, version-controlled reference datasets used as **competition index sources**
on [crowdsource](https://crowdsource.sh). These define *what* a competition asks
participants to predict (the set of index keys) — kept here, under our control,
rather than depending on third-party datasets that can go stale or disappear.

A daily GitHub Action ([`.github/workflows/refresh.yml`](.github/workflows/refresh.yml))
regenerates each snapshot from its upstream authority and commits only on change.

## Datasets

| Path | Keys | Source | Refresh |
| --- | --- | --- | --- |
| [`sp500/constituents.csv`](sp500/constituents.csv) | `Symbol` (S&P 500 members) | Wikipedia — [List of S&P 500 companies](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies) | daily |
| [`bikeshare/citibike/stations.csv`](bikeshare/citibike/stations.csv) | `station_id` (Citi Bike NYC docks) | [Citi Bike GBFS](https://gbfs.citibikenyc.com/gbfs/en/station_information.json) | daily |

`sp500/constituents.csv` columns: `Symbol, Security, GICS Sector, GICS Sub-Industry`.
`Symbol` is the index key (matched against Massive day-aggregate tickers at resolution).

`bikeshare/citibike/stations.csv` columns: `station_id, name, lat, lon, capacity`.
`station_id` is the index key (matched against the Citi Bike `station_status` feed at resolution).

## Usage

Competitions point their `input_url` at the raw file, e.g.:

```
https://raw.githubusercontent.com/1kbgz/crowdsource-datasets/main/sp500/constituents.csv
```

## Adding a dataset

Add `scripts/refresh_<name>.py` (write `<name>/<file>.csv`, sorted, with a sanity
floor on row count), wire it into the refresh workflow, and document it above.

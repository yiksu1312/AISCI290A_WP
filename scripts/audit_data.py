"""Inspect metadata and extract only one grid point per file, never full cubes."""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr


def audit(data_dir, output_dir):
    files = sorted(p for p in data_dir.rglob("*.nc") if not p.name.startswith("._"))
    if not files:
        raise FileNotFoundError(f"No NetCDF files found under {data_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    inventory, series, locations = [], {}, set()
    for path in files:
        with xr.open_dataset(path, engine="netcdf4") as ds:
            time = "valid_time" if "valid_time" in ds.coords else "time"
            dates = pd.DatetimeIndex(ds[time].values)
            lon_target = -117.8265 if float(ds.longitude.min()) < 0 else 242.1735
            point = ds.sel(latitude=33.6846, longitude=lon_target, method="nearest")
            location = (float(point.latitude), float(point.longitude))
            locations.add(location)
            item = {
                "file": path.relative_to(data_dir).as_posix(),
                "sizes": dict(ds.sizes), "attributes": dict(ds.attrs),
                "coordinates": {k: {"dims": list(v.dims), "attributes": dict(v.attrs)}
                                for k, v in ds.coords.items()},
                "latitude_range": [float(ds.latitude.min()), float(ds.latitude.max())],
                "longitude_range": [float(ds.longitude.min()), float(ds.longitude.max())],
                "selected_latitude": location[0], "selected_longitude": location[1],
                "start": str(dates.min()), "end": str(dates.max()),
                "time_monotonic": bool(dates.is_monotonic_increasing),
                "duplicate_times": int(dates.duplicated().sum()), "variables": {},
            }
            for name, var in ds.data_vars.items():
                info = {"dims": list(var.dims), "dtype": str(var.dtype),
                        "attributes": dict(var.attrs)}
                if time in var.dims and {"latitude", "longitude"}.issubset(var.dims):
                    local = point[name].squeeze(drop=True)
                    if local.dims != (time,):
                        raise ValueError(f"Unexpected point dimensions: {path.name}/{name}: {local.dims}")
                    values = local.to_series()
                    values.index = dates
                    values.index.name = "date"
                    series.setdefault(name, []).append(values.rename(name))
                    info["point_missing"] = int(values.isna().sum())
                    info["point_nonfinite"] = int((~np.isfinite(values)).sum())
                    info["point_min"] = float(values.min())
                    info["point_max"] = float(values.max())
                item["variables"][name] = info
            inventory.append(item)
    if len(locations) != 1:
        raise ValueError(f"Inconsistent grids selected: {locations}")
    columns = []
    for name, parts in series.items():
        joined = pd.concat(parts).sort_index()
        if joined.index.has_duplicates:
            raise ValueError(f"Duplicate dates for {name}")
        expected = pd.date_range(joined.index.min(), joined.index.max(), freq="D")
        if not joined.index.equals(expected):
            raise ValueError(f"Missing days or non-daily timestamps for {name}")
        columns.append(joined)
    if not all(s.index.equals(columns[0].index) for s in columns):
        raise ValueError("Variables do not share exactly the same dates")
    table = pd.concat(columns, axis=1)
    table.index.name = "date"
    summary = {
        "file_count": len(files), "selected_coordinates": list(next(iter(locations))),
        "rows": len(table), "start": str(table.index.min()), "end": str(table.index.max()),
        "missing_by_variable": table.isna().sum().to_dict(),
        "daily_continuity_and_alignment": "passed",
        "scope": "Metadata and selected-point checks; no full-grid missing-value scan.",
        "land_status": "Not verified by land-sea mask; no land-sea mask supplied.",
        "precipitation": "Preserved in source units; daily-mean must not be relabeled as daily accumulation.",
        "wind": "u/v components are retained; magnitude of daily-mean components is not mean scalar speed.",
    }
    table.to_csv(output_dir / "irvine_daily_source_units.csv")
    report = {"summary": summary, "files": inventory}
    (output_dir / "data_audit.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return report, table


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=project_root / "data/data")
    parser.add_argument("--output-dir", type=Path, default=project_root / "data/processed")
    args = parser.parse_args()
    audit(args.data_dir, args.output_dir)

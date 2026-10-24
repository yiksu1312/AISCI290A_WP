"""Inspect five small NetCDF members in place without extracting the archive."""
import argparse
import json
import tarfile
from pathlib import Path

import netCDF4
import xarray as xr

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("archive", type=Path)
parser.add_argument("--output", type=Path, default=Path("data/archive_sample_metadata.json"))
args = parser.parse_args()
results = []
with tarfile.open(args.archive) as archive:
    for member in archive.getmembers():
        if not (member.isfile() and "/2009_JanFeb/" in member.name
                and member.name.endswith(".nc") and not Path(member.name).name.startswith("._")):
            continue
        # One compressed NetCDF container (a few MB), not the full weather data cube.
        nc = netCDF4.Dataset("in_memory.nc", memory=archive.extractfile(member).read())
        with xr.open_dataset(xr.backends.NetCDF4DataStore(nc)) as ds:
            point = ds.sel(latitude=33.6846, longitude=-117.8265, method="nearest")
            results.append({
                "file": member.name, "sizes": dict(ds.sizes),
                "selected_latitude": float(point.latitude),
                "selected_longitude": float(point.longitude),
                "start": str(ds.valid_time.values[0]),
                "end": str(ds.valid_time.values[-1]),
                "attributes": dict(ds.attrs),
                "time_attributes": dict(ds.valid_time.attrs),
                "variables": {name: {"dims": list(var.dims), "attributes": dict(var.attrs)}
                              for name, var in ds.data_vars.items()},
            })
if not results:
    raise ValueError("Expected January-February 2009 members were not found")
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
print(f"Opened {len(results)} NetCDF members with netCDF4 and xarray; metadata saved to {args.output}")

"""Create training-period exploratory figures without fitting any models."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr


def make_figures(root):
    report = json.loads((root / "data/processed/data_audit.json").read_text(encoding="utf-8"))
    table = pd.read_csv(root / "data/processed/irvine_daily_source_units.csv", index_col="date", parse_dates=True)
    # Keep exploratory outcomes in 2009; reserve 2010 for subsequent split decisions.
    table = table.loc["2009"].copy()
    out = root / "reports/figures"
    out.mkdir(parents=True, exist_ok=True)
    units = {}
    for item in report["files"]:
        for name, meta in item["variables"].items():
            units[name] = meta["attributes"].get("units", "unknown")
    if units.get("t2m") != "K":
        raise ValueError("Temperature conversion requires verified Kelvin units")
    table["t2m"] -= 273.15
    units["t2m"] = "degrees C"
    fig, axes = plt.subplots(len(table.columns), 1, figsize=(12, 3 * len(table.columns)), sharex=True)
    for ax, name in zip(axes, table.columns):
        ax.plot(table.index, table[name], color="0.65", lw=0.8, label="Daily source value")
        ax.plot(table.index, table[name].rolling(3, min_periods=3).mean(), lw=1.2, label="Trailing 3-day mean")
        ax.plot(table.index, table[name].rolling(7, min_periods=7).mean(), lw=1.4, label="Trailing 7-day mean")
        ax.set_ylabel(f"{name} ({units[name]})")
        ax.grid(alpha=0.2)
    axes[0].legend(ncol=3, fontsize=9)
    axes[0].set_title("Grid point near Irvine: 2009 daily values and trailing means")
    axes[-1].set_xlabel("Date (source daily timestamp)")
    fig.tight_layout()
    fig.savefig(out / "irvine_2009_rolling.png", dpi=160)
    plt.close(fig)
    for name in ["t2m", "tp"]:
        item = next(f for f in report["files"] if name in f["variables"] and f["start"].startswith("2009-01"))
        with xr.open_dataset(root / "data/data" / item["file"]) as ds:
            time = "valid_time" if "valid_time" in ds.coords else "time"
            day = ds[name].isel({time: 0})
            if name == "t2m":
                day = day - 273.15
            fig, ax = plt.subplots(figsize=(11, 5))
            day.plot(ax=ax, cmap="coolwarm" if name == "t2m" else "Blues", cbar_kwargs={"label": f"{name} ({units[name]})"})
            lat, lon = report["summary"]["selected_coordinates"]
            ax.scatter([lon], [lat], marker="x", c="black", s=55, label="Selected grid point")
            ax.legend()
            ax.set_title(f"{name}: {str(ds[time].values[0])[:10]} — source daily statistic")
            ax.set_xlabel("Longitude (degrees east)")
            ax.set_ylabel("Latitude (degrees north)")
            fig.tight_layout()
            fig.savefig(out / f"{name}_2009_first_day.png", dpi=160)
            plt.close(fig)
    print("Created three exploratory figures from 2009; precipitation remains in source units.")


if __name__ == "__main__":
    make_figures(Path(__file__).resolve().parents[1])

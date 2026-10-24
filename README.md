# AISCI 290A — Weather prediction near Irvine

Yikai (Constantine) Su · UCI MAAIS · Instructor: Daniel Whiteson

**Question:** Can recent local weather improve next-day temperature predictions
near Irvine compared with a persistence baseline?

This is a retrospective forecast experiment using gridded ERA5 reanalysis,
not a real-time weather service or a precise Irvine weather station.

## Local project location

Active project: `C:\Users\giorg\Desktop\290A\Project1_WeatherPrediction`.
Open `Project1_WeatherPrediction.code-workspace` in VS Code. The former OneDrive
copy is retained as a backup; use this local Desktop copy for future work.

## Setup

The instructor's `environment.yml` was not found in the project or Downloads.
The included file is an explicit Windows-compatible project fallback, not a copy
of the instructor's configuration. It uses Python 3.12 and conda-forge.

```powershell
conda env create -f environment.yml
conda activate 290A
python -m ipykernel install --user --name aisci290a --display-name "Python (290A Weather)"
python scripts/verify_environment.py
python scripts/audit_data.py
python scripts/make_exploration.py
```

Do not recreate an existing environment blindly. Inspect `conda env list` first.
On this PC, open a PowerShell terminal in the project folder and run `. .\activate.ps1` to activate Conda without changing your global shell profile. Miniforge is installed under your user profile; it was deliberately not added to the global PATH.

In VS Code, open this project folder, select its configured interpreter and
the **Python (290A Weather)** notebook kernel. Local interpreter settings are
excluded from Git; extension recommendations are included.

## Data and structure

- `data/data/`: original course data location (60 NetCDF
  files in 12 two-month folders at initial inspection). The files are available in the local Desktop project; original archives and sidecars are preserved.
- `data/processed/`: local point table and full metadata audit, excluded from Git.
- `scripts/`: repeatable environment verification and data inspection.
- `notebooks/`: exploration using the same processing functions.
- `reports/`: verified setup notes and selected figures.
- `environment.yml`: portable dependency specification.

Obtain the supplied 2009–2010 continental-US subset from the course distribution.
The upstream [ERA5 daily statistics catalogue](https://cds.climate.copernicus.eu/datasets/derived-era5-single-levels-daily-statistics?tab=overview)
describes a larger collection; it does not establish the variables in this subset.
Place extracted files under `data/data/`, or pass `--data-dir` to the audit script.
Raw data, NetCDF files, archives, environments, and credentials are never committed.
The script ignores macOS `._` sidecar files and reads only coordinates, metadata,
and one selected point per variable. It does not load full data cubes.

## Method and limitations

Forecast origin: after today's daily values are available, predict tomorrow.
Check dates, duplicate records, missing days, and variable alignment before
shifting targets or calculating trailing 3-day/7-day means (including today).
Use chronological splits assigned by **target date**, and compare persistence,
temperature-only regression, and expanded regression on identical validation dates.
Fit all learned preprocessing on training data only; preserve the final test period.
The provisional 2009 train / early-2010 validation / late-2010 test split needs
justification because two years provide weak seasonal coverage.

Check precipitation metadata before conversion: files labeled daily-mean cannot
automatically be interpreted as mm/day. Keep wind components explicit; the
magnitude of averaged u/v is not the daily average of scalar wind speed.
Use a grid point near Irvine; land status requires separate verification.
No model scores or progress-presentation slot are assumed.

Later work: temperature change, spatial neighbors, small neural network,
2–3-day forecasts, precipitation baselines/regression, and high-temperature
classification with a fixed training-derived 75th-percentile threshold.
See `reports/setup_status.md` for verified progress and next steps.

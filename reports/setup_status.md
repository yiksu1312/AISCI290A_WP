# Setup and handoff — 2026-10-24

## Verified setup

- Project: `C:\Users\giorg\Desktop\290A\Project1_WeatherPrediction`.
- No applicable AGENTS.md was found in the inspected project/ancestor folders.
- Instructor environment.yml was not found in the project or Downloads. The committed configuration is a clearly labeled fallback.
- Miniforge 26.9.4 installed under `C:\Users\giorg\miniforge3`; new environment `290A`, Python 3.12.15. No pre-existing Conda environment was overwritten.
- Windows installer issue: conda-launchers had zero path records despite its binary existing. Reinstalling that package restored six records; subsequent environment creation returned success.
- Verified imports: numpy 2.5.4, pandas 3.1.0, matplotlib 3.11.2, seaborn 0.13.2, scikit-learn 1.9.1, xarray 2026.9.0, dask 2026.8.0, netCDF4 1.7.4, ipykernel 7.4.0, JupyterLab 4.6.4, nbconvert 7.17.2.
- A real `aisci290a` Jupyter kernel executed successfully and reported the environment interpreter. Display name: **Python (290A Weather)**.
- VS Code 1.141.0: Python, Pylance, Python Environments, and Jupyter extensions installed and listed. Project settings specify the interpreter and Conda executable; notebook metadata names the matching kernel. Interactive VS Code UI selection was not independently exercised.
- Git 2.45.1 and GitHub CLI 2.103.2 verified. Existing Git Credential Manager identity is `yiksu1312`.
- GitHub CLI persistent login rejected the existing token because it lacks `read:org`; no broader authorization requested. Existing credential worked for GitHub API repository creation via process-local GH_TOKEN. Git push uses the existing credential manager.
- A verified official portable GitHub CLI was also installed while the MSI installer was pending; the MSI subsequently completed successfully.
- Private repository: https://github.com/yiksu1312/AISCI290A_WP (API confirmed `private: true`).
- `.gitignore` preceded staging; raw data, NetCDF, archives, environments, credentials, and local interpreter settings are excluded.

## Data inspection completed

Initial inventory found 60 actual NetCDF files and 12 ZIP archives in `data/data/`, plus macOS `._` sidecars. The user subsequently confirmed they were reorganizing the files; the original month folders became empty. The final data location is now `C:\Users\giorg\Desktop\290A\Project1_WeatherPrediction\data\data`; see the migration record below.

The original `C:\Users\giorg\Downloads\data.tgz` remains available. Its inventory contains 60 NetCDF and 12 ZIP files, with no unsafe member paths. Five January-February 2009 NetCDF members were opened directly in memory using both netCDF4 and xarray. Only small file containers, coordinates, and metadata were read; full weather arrays were not loaded.

| Variable | Meaning | Source unit |
| --- | --- | --- |
| t2m | 2 m temperature | K |
| msl | Mean sea level pressure | Pa |
| u10 | 10 m eastward wind component | m s**-1 |
| v10 | 10 m northward wind component | m s**-1 |
| tp | Total precipitation, daily-mean processed | m |

Sample dimensions: valid_time=59, latitude=105, longitude=237. Grid spacing: 0.25 degrees. Latitude extent: 24 to 50 N; longitude extent: -125 to -66 (negative-west convention).

Nearest point to the chosen Irvine reference (33.6846, -117.8265): **33.75 N, 117.75 W**. This is a grid point near Irvine, not a weather station. Land status has not been verified against a coastline or land-sea mask; do not claim exact city/station representativeness.

All five sample histories record daily_reduce(..., how=mean). Temperature, pressure, and wind record time_shift=0 hours; precipitation records time_shift=-1 hour and GRIB_stepType=accum. Do not interpret tp as mm/day or assume equal temporal support solely from matching date labels. Confirm accumulation interval, input sampling frequency, and daily-window semantics with Daniel. Wind speed derived from mean components is not mean scalar wind speed.

## Validation scope and pending work

Passed: required imports, actual Jupyter kernel execution, five archived NetCDF files opened through both netCDF4 and xarray, notebook structural validation, Python script compilation, data exclusion checks.

Pending after migration: land status; temperature/precipitation maps and time series; rolling-average figures; model fitting and evaluation. The exploration notebook and plotting script are prepared but have NOT been executed end-to-end against the reorganized dataset. No model metrics or completed plots are claimed.

Continue from the verified local Desktop location:

1. Use `. .\activate.ps1` in a project PowerShell terminal.
2. Run `python scripts/audit_data.py` (defaults to the current project data directory).
3. Execute the notebook or plotting script; their relative data paths match the migrated layout.
4. Resolve precipitation temporal support before using it in forecasts; document any conversions.
5. Produce exploratory plots using 2009, define and justify chronological splits by target date, then compare persistence and regressions on identical validation dates. Keep the final test outcomes untouched.

To repeat the archive check without extracting data:

```powershell
python scripts/inspect_archive.py "$env:USERPROFILE\Downloads\data.tgz"
```

The planned progress-report date is October 27, 2026; slot and duration are unconfirmed. No email was sent.

## Migration to local Desktop — 2026-10-24

The active project is now outside OneDrive at `C:\Users\giorg\Desktop\290A\Project1_WeatherPrediction`. The old OneDrive project is retained as a backup; open the local Desktop copy for future work. Windows Desktop redirection and global OneDrive settings were not changed.

All 76 source project files, including Git history and local VS Code settings, were copied or matched by SHA-256. All 157 pre-existing destination files were verified unchanged. The destination contains 60 actual NetCDF and 12 ZIP files, excluding macOS sidecars. Git origin and the original HEAD were preserved.

Conda and the aisci290a kernel remain under the user profile outside OneDrive. Open `Project1_WeatherPrediction.code-workspace` or the project folder in VS Code. The workspace uses a relative folder path; the audit script defaults are anchored to its project root.

Post-migration verification passed: all 60 NetCDF files opened with xarray; 730 continuous daily timestamps from 2009-01-01 through 2010-12-31; no duplicate dates; equal date indexes across all five variables; no missing values at the selected grid point. This does not verify matching physical aggregation windows or full-grid completeness. The actual Jupyter kernel was re-executed successfully after relocation. Local processed outputs remain Git-ignored.

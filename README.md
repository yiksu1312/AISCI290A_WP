# Weather Prediction Near Irvine

Constantine Su | AI SCI 290A 

Instructor: Daniel Whiteson

Progress for October 27, 2026

## 1. The question

**Can recent local weather improve next-day temperature predictions near Irvine compared with assuming tomorrow will be like today?**

I chose Irvine because I live and study here. I am using the course-provided ERA5 data for 2009 and 2010. The supplied data cover temperature, pressure, precipitation, and wind across the continental US. My experiments so far use temperature only.

The current task is to predict tomorrow's daily mean temperature after today's daily values are available. I use the grid point at **33.75°N, 117.75°W**, near Irvine. This is gridded reanalysis data, not an Irvine weather station or a live forecast service. I still need to check the point's land location and how well it represents the area.

## 2. Exploratory

### Notebook guide

- **`notebooks/01_data_audit.ipynb` — loading data and checking dates.** This is where I started working with `glob` and `xarray`. In the loading walkthrough, I opened one temperature file, looked at its dimensions and the `t2m` variable, and then combined the 12 temperature files. I also worked through checking whether the dates were sorted, unique, and continuous.
- **`notebooks/02_temperature_only_v1.ipynb` — version 1: temperature only.** This is the notebook for the temperature exploration and first prediction experiment described below: maps, line plots, rolling averages, persistence, and temperature-only linear regression.

### What I explored

I loaded the temperature files using `xarray`, combined them by their coordinates, and converted temperature from Kelvin to Celsius by subtracting 273.15. The combined data have 730 daily timestamps from January 1, 2009 to December 31, 2010, with 105 latitudes and 237 longitudes.

I made several plots to get a feel for the data:

- **A temperature map for January 1, 2009.** The northern part of the plotted region was generally colder than the southern part.
- **A west-to-east line at 33.75°N.** Temperature varied substantially, but did not consistently increase or decrease from west to east.
- **A south-to-north line at 117.75°W.** Temperature generally decreased toward the north, with local rises and falls.

The two line plots were a chance to play around with selecting data and compare the spatial patterns along lines crossing the grid point near Irvine. They are exploratory exercises, not inputs to the current model. They show different locations on one day, not changes over time. Terrain could help explain some variation, but I have not checked that explanation.

I then plotted the **2009–2010 daily temperature series at the selected point**. Temperatures were generally higher in summer and lower in winter, with noticeable day-to-day fluctuations.

Finally, I calculated **trailing 3-day and 7-day averages** and plotted them with the daily temperatures. Both smooth the fluctuations; the 7-day average is smoother and responds more slowly to sudden changes. Each average includes today and preceding days only. These averages have been plotted but have **not yet been used in a regression model**.

## 3. Baseline and first model

### Prediction table and time split

I converted the local temperature series into a pandas DataFrame. Each row contains today's temperature and tomorrow's observed temperature, created using `shift(-1)` after checking daily continuity. Removing the final row with no next-day target leaves 729 samples.

I split samples by the **date being predicted**, not just the date of the input:

| Set | Target dates | Samples | Purpose |
| --- | --- | ---: | --- |
| Training | January 2–December 31, 2009 | 364 | Fit linear regression |
| Validation | January 1–June 30, 2010 | 181 | Compare predictions |
| Test | July 1–December 31, 2010 | 184 | Reserved for final evaluation |

This split is provisional. Validation and test cover different seasons, and two years provide limited seasonal coverage. I would like to discuss this choice with Daniel. The test set has been set aside but its prediction performance has not been evaluated.

### Persistence

**Predicted temperature tomorrow = observed temperature today.**

This baseline needs no training. I calculated its validation MAE and RMSE and plotted predictions against actual temperatures on the same target dates. The prediction follows the actual pattern with a one-day lag, making mistakes when temperature changes suddenly.

### Linear regression using today's temperature

I trained `LinearRegression()` on the training set with one input: today's temperature. The fitted equation is:

```text
Predicted temperature tomorrow = 0.953983 × today's temperature + 0.7772236
```

I used the fitted model to predict the same 181 validation targets as persistence.

| Model | Validation MAE (°C) | Validation RMSE (°C) |
| --- | ---: | ---: |
| Persistence | 0.901 | 1.148 |
| Linear regression: today's temperature | 0.873 | 1.129 |

Linear regression reduced MAE by about **3.1%** and RMSE by about **1.6%**. This is a small improvement on this validation period, not evidence that it will always perform better.

## 4. Status and plan

### Where I stopped

I have finished the initial temperature plots, rolling-average exploration, persistence evaluation, and the first temperature-only linear regression comparison. I am pausing here before adding more features. I have not yet trained a model with rolling averages, used the other weather variables, or evaluated the final test set.

### Immediate next step

Add the existing trailing 3-day and 7-day temperature averages as regression inputs alongside today's temperature. Handle their initial missing values, keep the same target-date split, and compare against the existing models on matching validation dates. The question is whether recent temperature history adds useful information beyond today's temperature.

### Overall project plan

1. **Temperature starting point — completed:** load temperature, explore it with plots, calculate rolling averages, and compare persistence with one-feature linear regression.
2. **Recent temperature history — next:** add the 3-day and 7-day averages to linear regression.
3. **Other local weather variables — planned:** inspect pressure, wind, and precipitation; align them in a daily table; make precipitation maps and time-series plots; add current values and trailing averages to the temperature model.
4. **Further temperature experiments — planned:** predict temperature change and reconstruct temperature, try neighboring grid points, try a small neural network, and extend forecasts to two and three days ahead.
5. **Other targets — planned:** study precipitation prediction with a simple baseline and attention to dry days; classify high-temperature days using a fixed 75th-percentile threshold calculated from training temperatures only.
6. **Final evaluation and presentation — planned:** choose the approach using validation results, evaluate it on the reserved test period, and organize the notebook, figures, and final video.

### Questions and things to resolve

- Is the chosen point on land and a reasonable representation of weather near Irvine?
- What is the exact precipitation aggregation and accumulation interval? I need to confirm this before labeling values as mm/day or using them in predictions.
- What time split is most useful with only two years and strong seasonal changes?

I am building this step by step with the Python, pandas, plotting, regression, and evaluation ideas from AI SCI 210, 220, and 290A. I will keep the README updated as the experiments progress.

## Working on the project

- `notebooks/`: loading practice and the main progress notebook.
- `data/data/`: course data, kept locally and excluded from GitHub.
- `environment.yml`: project dependencies.

Local project folder:

```text
C:\Users\giorg\Desktop\290A\Project1_WeatherPrediction
```

Open `Project1_WeatherPrediction.code-workspace` in VS Code and select **Python (290A Weather)** as the notebook kernel.

To activate the existing environment in a project PowerShell terminal:

```powershell
. .\activate.ps1
```

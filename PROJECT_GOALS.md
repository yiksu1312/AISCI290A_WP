# Where I tried the project goals

I organized the notebooks by what I was predicting. This table helps me find the code and plots for each part of the assignment.

| Goal | Where to look | What I tried |
| --- | --- | --- |
| Load and select parts of the data | 01; 02 sections 1-3; 03 sections 1-8 | Use xarray to open the NetCDF files, select dates, and choose the Irvine point. |
| Temperature map and temperature over time | 02 sections 2-3 | Plot one day on the grid, then follow one point over time. |
| Precipitation map and precipitation over time | 05 section 4 | Plot January 21, 2009 and the saved tp values with recent averages. |
| Choose one location | 02 section 3; 05 section 3 | Use 33.75 N, 117.75 W near Irvine. I still need to check whether the grid point is on land. |
| 3-day and 7-day averages, with plots | 02 section 3; 03 section 13; 04 section 12; 05 section 4 | Make averages for temperature, pressure, u, v, and tp using today and earlier days. |
| Linear regression for temperature, then more inputs | 02 sections 6-9; 03 sections 9-15 | Start with temperature and add averages and other weather information. |
| Try a neural network | 03 section 15; 05 section 23 | Try one small network for temperature and precipitation values. It does worse than linear regression here. |
| Predict the change instead of tomorrow's value | 03 section 15; 05 section 23 | Predict tomorrow minus today, then add today back. The linear predictions are the same when today's value is already an input. |
| Try information from nearby places | 03 section 14; 05 section 22 | Average today's temperature and tp over nine points in a 3 by 3 square. |
| Predict two and three days ahead | 03 section 16; 05 section 24 | Train a model for each number of days ahead. Check that the training answers would already be known when predicting. |
| Repeat the study for precipitation | 05 | Plot the data, predict positive or zero, then try averages, weather inputs, nearby points, the change, a small network, and longer predictions. |
| Predict hot days above the 75th percentile | 03 section 17 | Use the training temperatures to set the cutoff. Compare four methods and count how many hot days each finds. |

## What these results tell me

I compare the models on 181 days from January to June 2010. Some ideas helped and some did not. I include both kinds of results.

Notebook 06 checks an earlier set of chosen models on July-December 2010. I had already looked at those dates in a temperature test. It does not test all the extra models in 03 and 05, so I would need unused dates to check those models again.

For precipitation, I can predict the values saved in the files, but I still need to confirm how the daily averages were made before calling them daily rainfall totals. For hot days, there are only five in validation. A high accuracy by itself is not enough to show that the model can find them.

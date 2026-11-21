# Heatwave Attribution Results Data Inventory

## Scope and source files

This inventory describes the contents of `Heatwave attribution model results.zip`. The original ZIP and the project proposal were read without changing them. The proposal (`FDS_Review1_Final.docx`) is the only documentation available alongside the results. The archive has no README, data dictionary, model code, or source-data citations for individual columns. Where column names suggest a meaning but documentation does not define it, this inventory labels the meaning as tentative.

## Archive contents

| Archive entry | What it appears to contain |
|---|---|
| `attribution_by_event.csv` | Event-level heatwave details and attribution estimates. |
| `attribution_by_locality.csv` | Summaries of event-level attribution values for each locality. |
| `attribution_samples.npz` | A NumPy binary archive, likely containing arrays of model samples. Its internal array names and definitions are not documented here. |
| `cleaned_climate_dataset.csv.gz` | Compressed daily climate table. |
| `figures/fig1_study_area.png` | Study-area map/figure. |
| `figures/fig2_data_quality.png` | Data-quality figure. |
| `figures/fig3_gmst_and_heatwave_days.png` | Global-mean-temperature and heatwave-days figure. |
| `figures/fig4_skill_comparison.png` | Model-skill comparison figure. |
| `figures/fig5_reliability.png` | Reliability figure. |
| `figures/fig6_partial_dependence.png` | Partial-dependence figure. |
| `figures/fig7_attribution_events.png` | Event-attribution figure. |
| `figures/fig8_method_agreement.png` | Method-agreement figure. |
| `figures/fig9_uncertainty_sources.png` | Uncertainty-sources figure. |
| `heatwave_events_catalog.csv` | Catalog of detected heatwave events. |
| `localities.csv` | Locality names, districts, coordinates, and event/data-quality counts. |
| `metrics_heldout_localities.csv` | Predictive-skill metrics for a held-out-localities evaluation. |
| `metrics_heldout_years.csv` | Predictive-skill metrics for a held-out-years evaluation. |
| `results.json` | Run settings, summary statistics, evaluation metrics, and locality summaries. |

## CSV files, sizes, and missing values

“Rows” below means data rows, excluding the header. Missing values are blank CSV cells. Zero-filled missing-value counts do not prove that values are valid or correctly calculated.

| CSV file | Rows | Columns | Missing values |
|---|---:|---:|---|
| `attribution_by_event.csv` | 78 | 30 | None |
| `attribution_by_locality.csv` | 10 | 11 | 7 blanks, all in the seven numeric summary fields for Kanyakumari |
| `cleaned_climate_dataset.csv.gz` | 13,420 | 11 | 2,698 total: `tmax_imd_qc_C` 14; `tmax_era5_raw_C` 1,342; `tmax_era5_biascorr_C` 1,342 |
| `heatwave_events_catalog.csv` | 78 | 12 | None |
| `localities.csv` | 10 | 8 | None |
| `metrics_heldout_localities.csv` | 3 | 11 | None |
| `metrics_heldout_years.csv` | 3 | 11 | None |

The leading blank column name in each metrics CSV is not a missing data cell; it holds the model labels (for example, `B1 Logistic`).

## Column guide

The proposal describes the project as a counterfactual heat-attribution study and says the intended attribution output includes uncertainty. It does not provide an exact data dictionary or formulas for the archived field names. Descriptions below therefore separate clear units/roles from interpretations that still need confirmation.

### `attribution_by_event.csv`

| Columns | Beginner-friendly meaning |
|---|---|
| `event_id` | Identifier for this event. |
| `locality`, `district` | Place name and district label. |
| `lat`, `lon` | Latitude and longitude, presumably decimal degrees; coordinate reference is not stated. |
| `start_date`, `end_date`, `peak_date` | Event dates. |
| `duration_days` | Event duration in days. |
| `peak_tmax_C` | Highest reported daily maximum temperature for the event, in °C. |
| `peak_anomaly_C` | Peak temperature anomaly in °C; the baseline used for the anomaly is not specified in the archive. |
| `period` | Training or held-out time-period label. The archive’s JSON says training ends in 2015; rows label held-out events as 2016–2020. |
| `P_factual`, `P_counterfactual` | Names imply event probabilities under factual and counterfactual conditions. The proposal discusses counterfactual exceedance probabilities, but neither file defines these columns, their event threshold, denominator, or calculation. Treat them as probability-like outputs pending a code/data dictionary check, not as established probabilities. Values lie between about 0.135 and 0.556 in these rows. |
| `FAR_mean`, `FAR_median`, `FAR_sd`, `FAR_q05`, `FAR_q95`, `FAR_ci90_width` | Summary statistics and interval-width field for a quantity called FAR. The proposal does not define the acronym/formula or say how the percentiles were computed. These are **not safely interpretable as probabilities**: FAR means range from -0.421 to 0.044; q05 values are all negative and reach -2.524; reported 90% widths range from 0.769 to 2.906. A negative estimate or interval endpoint is incompatible with an ordinary probability. Confirm what FAR means, its scale, and whether interval labels are correct before using these fields. |
| `PR_median` | Median of a quantity called PR. No definition is provided. Do not assume it is a probability or a probability ratio. Values range from 0.921 to 1.098. |
| `dT_attributable_C_mean`, `dT_attributable_C_sd`, `dT_q05`, `dT_q95` | Names indicate a mean, spread, and quantiles for attributable temperature change in °C. The proposal describes a mean attributable-warming contribution and uncertainty, but does not define the exact calculation or interval procedure. The displayed units are temperature change, not probability. |
| `FAR_peakmag_mean`, `FAR_peakmag_sd` | Mean and spread of a peak-magnitude FAR variant, by name. Exact definition and units are absent. Do not treat as probability. |
| `n_samples` | Number of samples used in the event-level calculation, based on the name. It is 50 in all 78 rows. The proposal does not describe the sampling procedure. |
| `low_confidence_input` | Boolean flag for whether the input was marked low confidence; definition/threshold is not provided. |
| `data_mode` | Data-mode label; every row says `real`. The JSON labels inputs as CPC Tmax / NCEP-NCAR Z500 / IMD / HadCRUT5 / CMIP6. |

### `attribution_by_locality.csv`

| Columns | Beginner-friendly meaning |
|---|---|
| `locality` | Place being summarized. |
| `n_events` | Number of catalogued events used in the locality summary. |
| `FAR_mean`, `FAR_sd_mean`, `FAR_ci90_width_mean`, `FAR_q05_min`, `FAR_q95_max` | Locality-level summaries/ranges of the event-level FAR fields. Exact aggregation rules are not documented. As with the event table, FAR is undefined here and should not be called a probability. |
| `dT_mean_C` | Locality summary of the event-level attributable-temperature-change mean, in °C by name. Exact aggregation rule is undocumented. |
| `mean_duration_days` | Mean event duration in days. |
| `low_confidence` | Locality-level low-confidence flag; definition is not supplied. |
| `data_mode` | Data-mode label; all rows say `real`. |

Kanyakumari has zero events, so all seven numeric summary cells are blank. Those are expected “no estimate” blanks, not zero-valued estimates.

### `cleaned_climate_dataset.csv.gz`

| Columns | Beginner-friendly meaning |
|---|---|
| `date`, `locality` | Daily observation date and place. |
| `tmax_imd_qc_C` | Quality-checked IMD maximum temperature in °C; 14 rows are blank. |
| `tmax_era5_raw_C` | Raw ERA5 maximum temperature in °C; 1,342 rows are blank. |
| `tmax_era5_biascorr_C` | Bias-corrected ERA5 maximum temperature in °C; 1,342 rows are blank. The correction method is not documented in the archive. |
| `tmax_clean_C` | Selected/filled “clean” daily maximum temperature in °C; no blanks. The precise selection/fill rule is not supplied. |
| `imputed_from_era5` | Indicator for whether a value was imputed from ERA5; likely 0/1, based on observed values and name. |
| `normal_reference_period_C` | Reference normal temperature in °C; years used to calculate the normal are not specified. |
| `hw_threshold_C` | Heatwave temperature threshold in °C. JSON configuration gives `hw_abs` = 37°C; confirm how this column combines absolute and anomaly criteria. |
| `heatwave_day` | Heatwave-day indicator, represented as 0/1. The JSON configuration also lists an anomaly criterion (`hw_dep` = 2.5°C) and a minimum duration (`hw_min_days` = 2), but their exact application is not described. |
| `data_mode` | Data-mode label; values are `real`. |

The table covers 2010-03-01 through 2020-06-30 for 10 localities. The missing source fields may be expected where one source was unavailable or not used, but the fill logic needs confirmation.

### `heatwave_events_catalog.csv`

| Columns | Beginner-friendly meaning |
|---|---|
| `event_id`, `locality` | Event identifier and place. |
| `loc_idx` | Numeric locality index; mapping/order is not defined in this file. |
| `start_date`, `end_date`, `peak_date` | Event dates. |
| `duration_days` | Event duration in days. |
| `peak_tmax_C`, `peak_anom_C` | Peak maximum temperature and peak anomaly, in °C by name. Anomaly baseline is not stated here. |
| `imputed_share_event` | Share of event data marked as imputed; scale/denominator is not documented. |
| `period` | Training/held-out period label. |
| `data_mode` | Data-mode label; values are `real`. |

### `localities.csv`

| Columns | Beginner-friendly meaning |
|---|---|
| `locality`, `district` | Place name and district. |
| `lat`, `lon` | Latitude/longitude; coordinate reference not stated. |
| `imputed_share` | Share of climate values marked as imputed, apparently for the locality; denominator and calculation are not defined. |
| `low_confidence` | Locality confidence flag; rule not supplied. |
| `n_events` | Number of catalogued events. |
| `data_mode` | Data-mode label; values are `real`. |

### `metrics_heldout_localities.csv` and `metrics_heldout_years.csv`

Each contains three model rows. The metrics file with `heldout_localities` in its name appears to hold out localities; the other holds out years. The exact split construction is not documented.

| Columns | Beginner-friendly meaning |
|---|---|
| blank-name first column | Model name, such as logistic regression, gradient boosting, or CNN. |
| `n_rows`, `n_hw` | Number of evaluated rows and heatwave cases, by name. |
| `Brier`, `BSS` | Brier score and Brier skill score, common probability-forecast evaluation measures; baseline and exact calculation details are not documented. |
| `AUC` | Area under the ROC curve, a ranking/discrimination measure. |
| `LogLoss` | Logarithmic loss, a probability-forecast error measure. |
| `POD` | Probability of detection, also called hit rate/recall. |
| `FAR` | In these skill tables, likely false-alarm ratio given it appears alongside POD and CSI, but there is no data dictionary. Do not confuse this metric with the undefined `FAR_*` attribution fields. |
| `CSI` | Critical success index, a forecast hit/false-alarm/miss score. |
| `data_mode` | Data-mode label; all rows say `real`. |

## Attribution estimates and uncertainty: what the files support

- The proposal says the planned Stage 1 output is an uncertainty-aware attribution distribution, with a mean and uncertainty band. This supports the general idea that the result is meant to carry uncertainty, but it does **not** define the archived field formulas.
- The probability-like fields `P_factual` and `P_counterfactual` are within 0 and 1, but the archive does not define the event whose probability is measured or how either value was produced. Their names alone are not enough to establish the interpretation.
- `FAR` is not a probability in these files as currently represented. `FAR_mean` includes negative values, and quantiles and interval widths exceed the 0–1 range. The archive/proposal does not give the equation or units. The estimates may represent a transformed attribution metric or may indicate a calculation/labeling issue; the present files cannot decide which.
- `PR_median` is also undefined. Its values near 1 do not establish that it is a probability.
- The uncertainty fields are wide: event-level `FAR_ci90_width` has median about 1.28 and ranges up to 2.91; event-level `FAR_sd` median is about 0.44. Since the FAR scale and interval construction are undocumented, these numbers cannot yet be translated into plain-language confidence.
- `dT_*` fields carry °C labels and should be read as temperature-change estimates, not probabilities. But their formulas and sample/quantile methodology still need documentation.
- The JSON reports 50 samples per event in the production summary, while the event CSV reports `n_samples` = 50 for all rows. The NPZ sample arrays need to be inspected and matched to definitions before relying on the uncertainty summaries.

## Localities and whether comparisons are supported

There are 10 localities in `localities.csv`: Chennai, Mahabalipuram, Marakkanam, Cuddalore, Nagapattinam, Adirampattinam, Mimisal, Ramanathapuram, Thoothukudi, and Kanyakumari.

The event tables contain 78 events for only nine localities: Chennai 18, Mahabalipuram 13, Marakkanam 12, Cuddalore 9, Nagapattinam 8, Adirampattinam 8, Mimisal 8, Ramanathapuram 1, and Thoothukudi 1. Kanyakumari has zero events. Fifty events are labeled held-out (2016–2020), and 28 are labeled training (through 2015). The JSON reports 309 heatwave days, though the event catalog is the more direct source for the event counts.

This is enough for a **descriptive, preliminary comparison of event-attribution outputs** among localities with events, with substantial caution. The event counts are unbalanced, and two localities have only one event each; Kanyakumari cannot be compared on attribution at all. These are not independent, equally sized samples simply because rows are present. The summary table does not report uncertainty on locality-to-locality differences or account for different event counts. Also, some consistency checks in `results.json` are weak: its reported correlation between evaluation and production held-out FAR is -0.126, and its CNN correlations with the logistic and gradient-boosting methods are 0.082 and 0.247. These warrant investigation before ranking localities.

The files are **not sufficient for the proposal’s final vulnerability/allocation comparison**. They contain no locality-level social vulnerability, population exposure, health/adaptive-capacity measures, projected risk, intervention costs, or budget allocation outputs. They also do not document the formulas needed to interpret key attribution fields. A robust cross-locality conclusion should wait until those gaps and the small/uneven event counts are addressed.

## What to obtain before interpreting or modeling further

1. The analysis code and an exact data dictionary, especially formulas and units for `P_factual`, `P_counterfactual`, every `FAR` field, `PR_median`, `dT_*`, and the confidence/quality flags.
2. Documentation for `attribution_samples.npz`: array names, dimensions, meaning of each sample, and how samples produce means, standard deviations, and quantiles.
3. The event definition and threshold logic, anomaly reference period, imputation rules, bias-correction method, coordinate reference, and train/held-out split procedure.
4. Source and version/citation details for each input series, including how the JSON data label maps to the cleaned CSV columns.
5. For the later vulnerability comparison, suitable comparable locality-level exposure and socioeconomic/adaptive-capacity data, projected hazard data, and the agreed allocation rules and budget assumptions.

No final vulnerability model or allocation model is built in this inventory.

# Allocation-Rule Baselines and Comparison

Computes the four allocation rules (Section 5.5) on the same 10 coastal Tamil Nadu localities and compares their rankings (Section 5.6).

- (a) Historical vulnerability: Census 2011 composite index
- (b) Forecast risk: CMIP6 delta-change heatwave days
- (c) Attribution only: point estimate, uncertainty discarded
- (d) Attribution + uncertainty + equity (proposed)

## Run

```
pip install numpy pandas scipy matplotlib
python allocation_comparison.py
```

Takes a few seconds. Writes `outputs/` (CSVs, `summary.json`, `run_log.txt`) and `figures/` (8 PNGs).

## Inputs (`data/`)

- `attribution_by_event.csv`, `attribution_samples.npz`, `cleaned_climate_dataset.csv.gz`, `localities.csv`: attribution stage
- `HOUSING_DATA_RESULTS.csv`, `AGE_DATA_RESULTS.csv`, `equity_scores.csv`: equity stage
- `census2011_pca_localities.csv`: Census 2011 Primary Census Abstract, source URL per row
- `cmip6_ipcc_atlas_SAS/`: monthly South Asia land temperature, 33 CMIP6 models, from the IPCC-WG1/Atlas repository

## Updating after an attribution rerun

Replace `attribution_by_event.csv`, `attribution_samples.npz`, `cleaned_climate_dataset.csv.gz` and rerun. The script stops with an error if:

- samples are not in the same order as the events
- samples don't satisfy FAR = 1 - P0/P1
- the heatwave rule no longer reproduces the event catalogue

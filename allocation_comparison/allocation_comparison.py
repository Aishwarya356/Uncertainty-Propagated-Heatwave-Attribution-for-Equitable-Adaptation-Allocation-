"""
Allocation-Rule Baselines and Comparison
Uncertainty-Propagated Heatwave Attribution for Equitable Adaptation Allocation

Computes the four allocation rules of Review 1 (Section 5.5) on the same 10 coastal
Tamil Nadu localities and compares the resulting rankings (Section 5.6).

  (a) Historical-vulnerability-only   - Census 2011 composite vulnerability index
  (b) Forecast/projected-risk-only    - CMIP6 SSP2-4.5 delta-change heatwave days
  (c) Attribution-probability-only    - point-estimate attribution, uncertainty discarded
  (d) Attribution + uncertainty + equity (proposed)

Inputs (./data):
  attribution_by_event.csv, attribution_samples.npz,
  cleaned_climate_dataset.csv.gz, localities.csv          <- attribution stage
  HOUSING_DATA_RESULTS.csv, equity_scores.csv              <- equity stage
  census2011_pca_localities.csv                            <- Census 2011 PCA 
  cmip6_ipcc_atlas_SAS/cmip6_monthly_tas_SAS_land_*.csv    <- IPCC AR6 Atlas 

Run:  python p3_allocation_comparison.py
Outputs go to ./outputs (CSV/JSON) and ./figures (PNG).
Needs: numpy, pandas, scipy, matplotlib.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

ROOT = Path(__file__).resolve().parent
DATA, OUT, FIG = ROOT / "data", ROOT / "outputs", ROOT / "figures"
OUT.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)

# ----------------------------------------------------------------------------
# Configuration (all choices in one place)
# ----------------------------------------------------------------------------
LOCALITIES = ["Chennai", "Mahabalipuram", "Marakkanam", "Cuddalore", "Nagapattinam",
              "Adirampattinam", "Mimisal", "Ramanathapuram", "Thoothukudi", "Kanyakumari"]
OBS_YEARS = (2010, 2020)            # observed record from the attribution stage
FUTURE_PRIMARY = (2021, 2040)       # near-term planning horizon
FUTURE_ALT = (2041, 2060)           # mid-century sensitivity
SCENARIO_PRIMARY, SCENARIO_ALT = "ssp245", "ssp585"
MIN_RUN = 2                         # >= 2 consecutive heatwave days (attribution-stage definition)
LAMBDA_PRIMARY = 1.0                # equity weight in rule (d)
LAMBDAS = [0.0, 0.25, 0.5, 1.0, 2.0, 4.0]
TOP_K = 3
RULES = ["a", "b", "c", "d"]
RULE_NAMES = {
    "a": "(a) Historical vulnerability",
    "b": "(b) Forecast risk",
    "c": "(c) Attribution only",
    "d": "(d) Attribution + uncertainty + equity",
}
RULE_SHORT = {"a": "(a) Vulnerability", "b": "(b) Forecast", "c": "(c) Attribution", "d": "(d) Proposed"}

# Reference palette (dataviz skill, light mode): categorical slots 1-4, fixed order
SERIES = {"a": "#2a78d6", "b": "#eb6834", "c": "#1baf7a", "d": "#eda100"}
INK, INK2, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#8a8984", "#e4e3df", "#fcfcfb"
SEQ = LinearSegmentedColormap.from_list(
    "seq_blue", ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"])
DIV = LinearSegmentedColormap.from_list("div", ["#e34948", "#f0efec", "#2a78d6"])

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "text.color": INK, "axes.grid": False, "font.size": 9, "axes.titlesize": 10,
    "axes.titleweight": "bold", "axes.titlelocation": "left", "axes.spines.top": False,
    "axes.spines.right": False, "legend.frameon": False, "figure.dpi": 150,
})


def minmax(s):
    s = pd.Series(s, dtype=float)
    rng = s.max() - s.min()
    return (s - s.min()) / rng if rng > 0 else s * 0.0


def ranks_desc(s):
    """Rank 1 = highest priority; ties share the average rank."""
    return pd.Series(s).rank(ascending=False, method="average")


def shares(s):
    s = pd.Series(s, dtype=float).clip(lower=0)
    return s / s.sum()


# ----------------------------------------------------------------------------
# 1. Load inputs
# ----------------------------------------------------------------------------
events = pd.read_csv(DATA / "attribution_by_event.csv")
npz = np.load(DATA / "attribution_samples.npz")
far_s = npz["far_samples"].astype(float)                       # (78 events, 50 samples)
assert (npz["event_id"] == events["event_id"].values).all(), "sample/event order mismatch"
assert np.allclose(far_s, 1 - npz["P0_samples"] / npz["P1_samples"], atol=1e-4)
N_SAMPLES = far_s.shape[1]

climate = pd.read_csv(DATA / "cleaned_climate_dataset.csv.gz", parse_dates=["date"])
census = pd.read_csv(DATA / "census2011_pca_localities.csv").set_index("locality").loc[LOCALITIES]
housing = pd.read_csv(DATA / "HOUSING_DATA_RESULTS.csv", encoding="utf-8-sig").set_index("locality").loc[LOCALITIES]
p2_equity = pd.read_csv(DATA / "equity_scores.csv", encoding="utf-8-sig").set_index("locality").loc[LOCALITIES]
cmip = pd.read_csv(DATA / "cmip6_ipcc_atlas_SAS" / "cmip6_monthly_tas_SAS_land_1995_2100.csv",
                   parse_dates=["date"])

# ----------------------------------------------------------------------------
# 2. Rule (a): historical vulnerability index (Census 2011)
# ----------------------------------------------------------------------------
ind = pd.DataFrame(index=LOCALITIES)
ind["child_0_6_share"] = census["children_0_6"] / census["total_population"]
ind["illiteracy_pct"] = 100 - census["literacy_rate_pct"]
ind["sc_st_pct"] = census["sc_pct"] + census["st_pct"]
ind["non_worker_share"] = 1 - census["total_workers"] / census["total_population"]
ind["marginal_worker_pct"] = census["marginal_workers_pct"]
ind["no_electricity_pct"] = pd.to_numeric(housing["electricity_not_available_percent"], errors="coerce")
ind["water_away_pct"] = pd.to_numeric(housing["water_away_percent"], errors="coerce")

DOMAINS = {
    "sensitivity": ["child_0_6_share"],
    "socioeconomic": ["illiteracy_pct", "sc_st_pct", "non_worker_share", "marginal_worker_pct"],
    "housing": ["no_electricity_pct", "water_away_pct"],
}
norm = ind.apply(minmax)                      # 0-1 across the 10 localities, higher = worse
dom = pd.DataFrame({d: norm[cols].mean(axis=1, skipna=True) for d, cols in DOMAINS.items()})
dom.loc[norm[DOMAINS["housing"]].isna().all(axis=1), "housing"] = np.nan
V = dom.mean(axis=1, skipna=True)             # equal domain weights; missing domain dropped
n_domains = dom.notna().sum(axis=1)

# Equity weight for rule (d): adaptive-capacity deficit only (socioeconomic + housing),
# deliberately excluding the demographic-sensitivity domain so it is not identical to (a).
E = minmax(dom[["socioeconomic", "housing"]].mean(axis=1, skipna=True))

vuln = pd.concat([ind.round(4), norm.add_prefix("norm_").round(4),
                  dom.add_prefix("domain_").round(4)], axis=1)
vuln["vulnerability_index_V"] = V.round(4)
vuln["equity_weight_E"] = E.round(4)
vuln["domains_available"] = n_domains
vuln.index.name = "locality"
vuln.to_csv(OUT / "rule_a_vulnerability_index.csv")

# ----------------------------------------------------------------------------
# 3. Rule (b): forecast / projected risk (CMIP6 delta-change)
# ----------------------------------------------------------------------------
def heatwave_days(tmax, thr, dates, locs):
    """Flag heatwave days: Tmax >= threshold on >= MIN_RUN consecutive days in a season."""
    df = pd.DataFrame({"loc": np.asarray(locs), "date": pd.to_datetime(np.asarray(dates)),
                       "hot": (np.asarray(tmax) >= np.asarray(thr)).astype(int)})
    df = df.sort_values(["loc", "date"])
    grp = (df["loc"] + df["date"].dt.year.astype(str))
    # a new run starts whenever 'hot' changes, the season changes, or the day gap > 1
    gap = df["date"].diff().dt.days.ne(1)
    run_id = (df["hot"].diff().ne(0) | grp.ne(grp.shift()) | gap).cumsum()
    run_len = df.groupby(run_id)["hot"].transform("size")
    df["hw"] = ((df["hot"] == 1) & (run_len >= MIN_RUN)).astype(int)
    return df.sort_index()["hw"].values


clim = climate[climate["locality"].isin(LOCALITIES)].reset_index(drop=True)
n_seasons = OBS_YEARS[1] - OBS_YEARS[0] + 1
obs_hw = heatwave_days(clim["tmax_clean_C"].values, clim["hw_threshold_C"].values,
                       clim["date"], clim["locality"].values)
# Check: runs of >= MIN_RUN hot days must reproduce the attribution stage's 78-event catalogue
_tmp = clim.assign(hw=obs_hw).sort_values(["locality", "date"])
_starts = (_tmp["hw"].diff().fillna(_tmp["hw"]).eq(1) | _tmp["locality"].ne(_tmp["locality"].shift())) & _tmp["hw"].eq(1)
N_OBS_EVENTS = int(_starts.sum())
assert N_OBS_EVENTS == len(events), f"event definition does not reproduce the attribution catalogue ({N_OBS_EVENTS} vs {len(events)})"

complete = cmip.groupby("model")["experiment"].nunique()
models = sorted(complete[complete == 3].index)


def model_deltas(scenario, window):
    """Monthly (Mar-Jun) warming of South Asia land tas: future window minus 2010-2020."""
    rows = {}
    for m in models:
        g = cmip[(cmip["model"] == m) & cmip["experiment"].isin(["historical", scenario])].copy()
        g = g[~((g["experiment"] == "historical") & (g["date"].dt.year > 2014))]
        g = g[~((g["experiment"] == scenario) & (g["date"].dt.year <= 2014))]
        g["year"], g["month"] = g["date"].dt.year, g["date"].dt.month
        g = g[g["month"].isin([3, 4, 5, 6])]
        base = g[g["year"].between(*OBS_YEARS)].groupby("month")["tas_SAS_land_C"].mean()
        fut = g[g["year"].between(*window)].groupby("month")["tas_SAS_land_C"].mean()
        rows[m] = fut - base
    return pd.DataFrame(rows).T                  # models x months


def projected_hw(scenario, window):
    deltas = model_deltas(scenario, window)
    month = clim["date"].dt.month.values
    per_model = {}
    for m, d in deltas.iterrows():
        shifted = clim["tmax_clean_C"].values + d.reindex(month).values
        hw = heatwave_days(shifted, clim["hw_threshold_C"].values, clim["date"], clim["locality"].values)
        per_model[m] = pd.Series(hw).groupby(clim["locality"].values).sum() / n_seasons
    pm = pd.DataFrame(per_model).loc[LOCALITIES]
    return pm, deltas


fc_primary, deltas_primary = projected_hw(SCENARIO_PRIMARY, FUTURE_PRIMARY)
fc_585, deltas_585 = projected_hw(SCENARIO_ALT, FUTURE_PRIMARY)
fc_mid, deltas_mid = projected_hw(SCENARIO_PRIMARY, FUTURE_ALT)

obs_days = pd.Series(obs_hw).groupby(clim["locality"].values).sum().loc[LOCALITIES] / n_seasons
F = fc_primary.median(axis=1)
forecast = pd.DataFrame({
    "observed_hw_days_per_season_2010_2020": obs_days.round(2),
    "F_ssp245_2021_2040_median": F.round(2),
    "F_ssp245_2021_2040_p10": fc_primary.quantile(0.10, axis=1).round(2),
    "F_ssp245_2021_2040_p90": fc_primary.quantile(0.90, axis=1).round(2),
    "F_ssp585_2021_2040_median": fc_585.median(axis=1).round(2),
    "F_ssp245_2041_2060_median": fc_mid.median(axis=1).round(2),
    "shares_IMD_grid_cell_with": ["", "", "", "", "Adirampattinam, Mimisal", "Nagapattinam, Mimisal",
                                  "Nagapattinam, Adirampattinam", "", "", ""],
})
forecast.index.name = "locality"
forecast.to_csv(OUT / "rule_b_forecast_risk.csv")
delta_summary = pd.DataFrame({
    "scenario_window": ["SSP2-4.5 2021-2040", "SSP5-8.5 2021-2040", "SSP2-4.5 2041-2060"],
    "n_models": [len(models)] * 3,
    "median_MarJun_warming_C": [d.mean(axis=1).median() for d in (deltas_primary, deltas_585, deltas_mid)],
    "p10_C": [d.mean(axis=1).quantile(0.1) for d in (deltas_primary, deltas_585, deltas_mid)],
    "p90_C": [d.mean(axis=1).quantile(0.9) for d in (deltas_primary, deltas_585, deltas_mid)],
}).round(3)
delta_summary.to_csv(OUT / "rule_b_cmip6_warming_deltas.csv", index=False)

# ----------------------------------------------------------------------------
# 4. Rules (c) and (d): attribution
#    PN = max(0, 1 - P0/P1) = probability of necessity (Hannart et al., 2016)
# ----------------------------------------------------------------------------
loc_of_event = events["locality"].values
pn_point = np.clip(events["FAR_mean"].values, 0, None)          # PN of the point estimate
pn_samples = np.clip(far_s, 0, None)                            # PN per sample

C = pd.Series(pn_point).groupby(loc_of_event).sum().reindex(LOCALITIES).fillna(0.0)

A = pd.DataFrame(pn_samples).groupby(loc_of_event).sum().reindex(LOCALITIES).fillna(0.0)  # loc x sample
mu, sd = A.mean(axis=1), A.std(axis=1, ddof=1)
cv = (sd / mu).where(mu > 0)
U = (mu / (1 + cv)).fillna(0.0)                                 # uncertainty-penalised attribution
U_norm = U / U.max()


def rule_d(lam, u=U_norm, e=E):
    return u * (1 + lam * e)


D = rule_d(LAMBDA_PRIMARY)

n_events = pd.Series(loc_of_event).value_counts().reindex(LOCALITIES).fillna(0).astype(int)
p_pos = pd.Series((far_s > 0).mean(axis=1)).groupby(loc_of_event).mean().reindex(LOCALITIES)
attr = pd.DataFrame({
    "n_events": n_events,
    "C_attribution_only_sum_PN_point": C.round(4),
    "A_mean_sum_PN_over_samples": mu.round(4),
    "A_sd": sd.round(4),
    "A_q05": A.quantile(0.05, axis=1).round(4),
    "A_q95": A.quantile(0.95, axis=1).round(4),
    "A_cv": cv.round(4),
    "U_uncertainty_adjusted": U.round(4),
    "U_normalised": U_norm.round(4),
    "mean_P_FAR_positive": p_pos.round(3),
    "E_equity_weight": E.round(4),
    "D_proposed_lambda_1": D.round(4),
})
attr.index.name = "locality"
attr.to_csv(OUT / "rules_c_d_attribution.csv")

# ----------------------------------------------------------------------------
# 5. Four-way comparison
# ----------------------------------------------------------------------------
scores = pd.DataFrame({"a": V, "b": F, "c": C, "d": D}).loc[LOCALITIES]
ranks = scores.apply(ranks_desc)
budget = scores.apply(shares)

table = pd.DataFrame(index=LOCALITIES)
for r in RULES:
    table[f"score_{r}"] = scores[r].round(4)
    table[f"rank_{r}"] = ranks[r]
    table[f"budget_share_pct_{r}"] = (100 * budget[r]).round(1)
table.index.name = "locality"
table.to_csv(OUT / "four_rule_rankings_and_budget_shares.csv")


def pair_stats(x, y):
    rho, p_rho = stats.spearmanr(x, y)
    tau, p_tau = stats.kendalltau(x, y)
    return rho, p_rho, tau, p_tau


pairs = []
for i, r1 in enumerate(RULES):
    for r2 in RULES[i + 1:]:
        rho, prho, tau, ptau = pair_stats(scores[r1], scores[r2])
        top1 = set(ranks[r1].nsmallest(TOP_K).index)
        top2 = set(ranks[r2].nsmallest(TOP_K).index)
        pairs.append({
            "rule_1": RULE_NAMES[r1], "rule_2": RULE_NAMES[r2],
            "spearman_rho": round(rho, 3), "spearman_p": round(prho, 3),
            "kendall_tau": round(tau, 3), "kendall_p": round(ptau, 3),
            f"top{TOP_K}_overlap": len(top1 & top2),
            "mean_abs_rank_shift": round((ranks[r1] - ranks[r2]).abs().mean(), 2),
            "max_abs_rank_shift": (ranks[r1] - ranks[r2]).abs().max(),
            "budget_moved_pct": round(50 * (budget[r1] - budget[r2]).abs().sum(), 1),
        })
pairs = pd.DataFrame(pairs)
pairs.to_csv(OUT / "pairwise_rank_agreement.csv", index=False)

rho_mat = scores.corr(method="spearman")
tau_mat = scores.corr(method="kendall")

# Ablation: which ingredient of (d) moves the ranking?
ablation_variants = {
    "c: point estimate, no uncertainty, no equity": C,
    "d0: + uncertainty propagation (E[PN], no penalty)": mu,
    "d1: + uncertainty penalty (U), lambda=0": U_norm,
    "d: + equity, lambda=1 (proposed)": D,
}
abl = []
prev = None
for name, s in ablation_variants.items():
    row = {"variant": name,
           "spearman_vs_c": round(stats.spearmanr(s, C)[0], 3),
           "spearman_vs_previous": round(stats.spearmanr(s, prev)[0], 3) if prev is not None else np.nan,
           "top3": ", ".join(ranks_desc(s).nsmallest(TOP_K).index)}
    abl.append(row)
    prev = s
abl = pd.DataFrame(abl)
abl.to_csv(OUT / "ablation_uncertainty_vs_equity.csv", index=False)

# Sensitivity 1: equity weight lambda
lam_rows, lam_ranks = [], {}
for lam in LAMBDAS:
    d = rule_d(lam)
    lam_ranks[lam] = ranks_desc(d)
    row = {"lambda": lam}
    for r in ["a", "b", "c"]:
        row[f"spearman_vs_{r}"] = round(stats.spearmanr(d, scores[r])[0], 3)
    row["top3"] = ", ".join(lam_ranks[lam].nsmallest(TOP_K).index)
    lam_rows.append(row)
lam_df = pd.DataFrame(lam_rows)
lam_df.to_csv(OUT / "sensitivity_lambda.csv", index=False)
lam_rank_df = pd.DataFrame(lam_ranks).loc[LOCALITIES]
lam_rank_df.columns = [f"rank_lambda_{l}" for l in LAMBDAS]
lam_rank_df.index.name = "locality"
lam_rank_df.to_csv(OUT / "sensitivity_lambda_ranks.csv")

# Sensitivity 2: alternative specifications of each baseline / ingredient
alt = {
    "b: SSP5-8.5 2021-2040": fc_585.median(axis=1),
    "b: SSP2-4.5 2041-2060": fc_mid.median(axis=1),
    "a: housing domain dropped": dom[["sensitivity", "socioeconomic"]].mean(axis=1),
    "d: equity = full vulnerability index V": rule_d(LAMBDA_PRIMARY, e=minmax(V)),
    "d: no uncertainty penalty (E[PN] x equity)": (mu / mu.max()) * (1 + LAMBDA_PRIMARY * E),
}
sens_rows = []
for name, s in alt.items():
    base = name.split(":")[0]
    ref = scores[base]
    sens_rows.append({"variant": name, "spearman_vs_primary_version": round(stats.spearmanr(s, ref)[0], 3),
                      "spearman_vs_d": round(stats.spearmanr(s, D)[0], 3),
                      "top3": ", ".join(ranks_desc(s).nsmallest(TOP_K).index)})
sens = pd.DataFrame(sens_rows)
sens.to_csv(OUT / "sensitivity_alternative_specifications.csv", index=False)

# Rank uncertainty for rule (d): propagate each of the 50 attribution samples
U_s = A.div(mu.max())                          # per-sample attribution on the same scale
rank_s = (U_s.mul(1 + LAMBDA_PRIMARY * E, axis=0)).rank(ascending=False, method="average")
rank_unc = pd.DataFrame({
    "rank_d_point": ranks["d"],
    "rank_median_over_samples": rank_s.median(axis=1),
    "rank_q05": rank_s.quantile(0.05, axis=1),
    "rank_q95": rank_s.quantile(0.95, axis=1),
    f"P_top{TOP_K}": (rank_s <= TOP_K).mean(axis=1).round(2),
})
rank_unc.index.name = "locality"
rank_unc.to_csv(OUT / "rule_d_rank_uncertainty.csv")
rank_unc_c = (pd.DataFrame(pn_samples).groupby(loc_of_event).sum().reindex(LOCALITIES).fillna(0)
              .rank(ascending=False, method="average"))

# Cross-check with the 4-unit partial equity index
p2 = pd.to_numeric(p2_equity["candidate_equity_score_0_to_1"], errors="coerce").dropna()
p2_check = {"localities": list(p2.index),
            "spearman_V_vs_partial_equity_index": round(stats.spearmanr(V[p2.index], p2)[0], 3)}

summary = {
    "n_localities": len(LOCALITIES),
    "n_events": int(len(events)),
    "n_attribution_samples": N_SAMPLES,
    "n_cmip6_models": len(models),
    "cmip6_models": models,
    "lambda_primary": LAMBDA_PRIMARY,
    "spearman_matrix": rho_mat.round(3).to_dict(),
    "kendall_matrix": tau_mat.round(3).to_dict(),
    "top3": {RULE_NAMES[r]: list(ranks[r].nsmallest(TOP_K).index) for r in RULES},
    "corr_V_E_spearman": round(stats.spearmanr(V, E)[0], 3),
    "equity_crosscheck": p2_check,
    "observed_event_days": int(obs_hw.sum()),
    "observed_events_reproduced": N_OBS_EVENTS,
}
(OUT / "summary.json").write_text(json.dumps(summary, indent=1))

# ----------------------------------------------------------------------------
# 6. Figures
# ----------------------------------------------------------------------------
def save(fig, name):
    fig.savefig(FIG / name, bbox_inches="tight", dpi=200)
    plt.close(fig)


short = {"Mahabalipuram": "Mahabalipuram", "Adirampattinam": "Adirampattinam",
         "Ramanathapuram": "Ramanathapuram"}

# Fig 1 - vulnerability indicators (normalised) + index
labels = {"child_0_6_share": "Children 0-6", "illiteracy_pct": "Illiteracy",
          "sc_st_pct": "SC/ST share", "non_worker_share": "Non-workers",
          "marginal_worker_pct": "Marginal workers", "no_electricity_pct": "No electricity",
          "water_away_pct": "Water fetched away"}
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.2), gridspec_kw={"width_ratios": [2.3, 1], "wspace": 0.45})
mat = norm[list(labels)].T
im = ax1.imshow(mat.values, cmap=SEQ, vmin=0, vmax=1, aspect="auto")
ax1.set_xticks(range(len(LOCALITIES)), LOCALITIES, rotation=45, ha="right")
ax1.set_yticks(range(len(labels)), list(labels.values()))
for (i, j), v in np.ndenumerate(mat.values):
    ax1.text(j, i, "n/a" if np.isnan(v) else f"{v:.2f}", ha="center", va="center", fontsize=7,
             color=MUTED if np.isnan(v) else ("white" if v > 0.55 else INK))
ax1.set_title("Indicators, scaled 0-1 across localities (1 = most vulnerable)")
for s in ax1.spines.values():
    s.set_visible(False)
order = V.sort_values()
ax2.barh([f"{l}*" if n_domains[l] < 3 else l for l in order.index], order.values, color=SERIES["a"], height=0.6)
for y, v in enumerate(order.values):
    ax2.text(v + 0.01, y, f"{v:.2f}", va="center", fontsize=8, color=INK2)
ax2.set_xlim(0, max(0.9, order.max() + 0.12))
ax2.set_title("Vulnerability index V (rule a)")
ax2.text(0, -0.16, "* housing data unavailable; mean of 2 domains", transform=ax2.transAxes, fontsize=7, color=MUTED)
ax2.tick_params(axis="y", length=0)
save(fig, "fig1_rule_a_vulnerability.png")

# Fig 2 - forecast risk
fig, ax = plt.subplots(figsize=(8.5, 3.9))
x = np.arange(len(LOCALITIES))
ax.bar(x, F.values, width=0.55, color=SERIES["b"], label="SSP2-4.5, 2021-2040 (median of 33 models)")
ax.errorbar(x, F.values, yerr=[F.values - fc_primary.quantile(0.1, axis=1).values,
                               fc_primary.quantile(0.9, axis=1).values - F.values],
            fmt="none", ecolor=INK2, elinewidth=1, capsize=3, label="10-90% model range")
ax.scatter(x, obs_days.values, s=40, color=INK, zorder=3, label="Observed 2010-2020")
ax.set_xticks(x, LOCALITIES, rotation=45, ha="right")
ax.set_ylabel("Heatwave days per Mar-Jun season")
ax.yaxis.grid(True, color=GRID, lw=0.8)
ax.set_axisbelow(True)
ax.set_title("Rule (b): projected heatwave days (CMIP6 delta-change on observed Tmax)")
ax.legend(loc="upper right", fontsize=8)
save(fig, "fig2_rule_b_forecast_risk.png")

# Fig 3 - attribution: point estimate vs propagated distribution
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.1), sharey=True)
y = np.arange(len(LOCALITIES))[::-1]
ax1.barh(y, C.values, color=SERIES["c"], height=0.55)
ax1.set_yticks(y, LOCALITIES)
ax1.set_title("Rule (c): sum of PN from point-estimate FAR")
ax1.set_xlabel("Attributable events (point estimate)")
ax1.xaxis.grid(True, color=GRID, lw=0.8)
ax1.set_axisbelow(True)
for yy, v in zip(y, C.values):
    ax1.text(v + 0.001, yy, f"{v:.3f}", va="center", fontsize=7, color=INK2)
ax2.hlines(y, A.quantile(0.05, axis=1), A.quantile(0.95, axis=1), color=MUTED, lw=2, label="5-95% of 50 samples")
ax2.scatter(mu.values, y, s=36, color=INK, zorder=3, label="Mean over samples")
ax2.scatter(U.values, y, s=44, marker="D", color=SERIES["d"], zorder=4, label="Uncertainty-penalised U")
ax2.set_title("Rule (d) input: PN propagated over 50 samples")
ax2.set_xlabel("Attributable events (sum of PN per sample)")
ax2.xaxis.grid(True, color=GRID, lw=0.8)
ax2.set_axisbelow(True)
ax2.legend(loc="lower right", fontsize=7.5)
ax2.tick_params(axis="y", length=0)
save(fig, "fig3_rules_c_d_attribution.png")

# Fig 4 - rank table (localities x rules)
fig, ax = plt.subplots(figsize=(6.4, 4.6))
rk = ranks[RULES].values
ax.imshow(rk, cmap=SEQ.reversed(), vmin=1, vmax=10, aspect="auto")
for (i, j), v in np.ndenumerate(rk):
    ax.text(j, i, f"{v:g}", ha="center", va="center", fontsize=9, color="white" if v <= 4 else INK)
ax.set_xticks(range(4), [RULE_SHORT[r] for r in RULES], rotation=20, ha="right")
ax.set_yticks(range(len(LOCALITIES)), LOCALITIES)
ax.set_title("Priority rank under each rule (1 = highest priority)")
for s in ax.spines.values():
    s.set_visible(False)
ax.tick_params(length=0)
save(fig, "fig4_rank_table.png")

# Fig 5 - Spearman and Kendall matrices
fig, axes = plt.subplots(1, 2, figsize=(9, 3.9))
for ax, mat_, nm in zip(axes, [rho_mat, tau_mat], ["Spearman's rho", "Kendall's tau"]):
    ax.imshow(mat_.values, cmap=DIV, vmin=-1, vmax=1)
    for (i, j), v in np.ndenumerate(mat_.values):
        ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=9,
                color="white" if abs(v) > 0.7 else INK)
    ax.set_xticks(range(4), ["(a)", "(b)", "(c)", "(d)"])
    ax.set_yticks(range(4), [RULE_SHORT[r] for r in RULES])
    ax.set_title(f"{nm} between rules")
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
save(fig, "fig5_rank_correlations.png")

# Fig 6 - budget shares
fig, ax = plt.subplots(figsize=(10, 4.2))
w = 0.2
for k, r in enumerate(RULES):
    ax.bar(np.arange(len(LOCALITIES)) + (k - 1.5) * w, 100 * budget[r].values, width=w - 0.02,
           color=SERIES[r], label=RULE_NAMES[r])
ax.set_xticks(np.arange(len(LOCALITIES)), LOCALITIES, rotation=45, ha="right")
ax.set_ylabel("Share of the same budget ceiling (%)")
ax.yaxis.grid(True, color=GRID, lw=0.8)
ax.set_axisbelow(True)
ax.set_title("Budget share under each allocation rule (shares proportional to rule score)")
ax.legend(fontsize=8, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.32))
save(fig, "fig6_budget_shares.png")

# Fig 7 - lambda sensitivity
fig, ax = plt.subplots(figsize=(7.2, 4.6))
lr = lam_rank_df.values
ax.imshow(lr, cmap=SEQ.reversed(), vmin=1, vmax=10, aspect="auto")
for (i, j), v in np.ndenumerate(lr):
    ax.text(j, i, f"{v:g}", ha="center", va="center", fontsize=9, color="white" if v <= 4 else INK)
ax.set_xticks(range(len(LAMBDAS)), [f"λ={l:g}" for l in LAMBDAS])
ax.set_yticks(range(len(LOCALITIES)), LOCALITIES)
ax.set_title("Rule (d) rank as the equity weight λ increases")
ax.tick_params(length=0)
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig7_lambda_sensitivity.png")

# Fig 8 - rank uncertainty (d) vs (c)
fig, ax = plt.subplots(figsize=(8, 4.3))
y = np.arange(len(LOCALITIES))[::-1]
ax.hlines(y + 0.15, rank_s.quantile(0.05, axis=1), rank_s.quantile(0.95, axis=1), color=SERIES["d"], lw=2.5)
ax.scatter(rank_s.median(axis=1), y + 0.15, color=SERIES["d"], s=40, zorder=3,
           label="(d) proposed: median and 5-95% rank over 50 samples")
ax.hlines(y - 0.15, rank_unc_c.quantile(0.05, axis=1), rank_unc_c.quantile(0.95, axis=1), color=SERIES["c"], lw=2.5)
ax.scatter(rank_unc_c.median(axis=1), y - 0.15, color=SERIES["c"], s=40, zorder=3,
           label="Attribution alone, per sample (no equity)")
ax.set_yticks(y, LOCALITIES)
ax.set_xlim(0.5, 10.5)
ax.set_xticks(range(1, 11))
ax.invert_xaxis()
ax.set_xlabel("Priority rank (1 = highest)")
ax.xaxis.grid(True, color=GRID, lw=0.8)
ax.set_axisbelow(True)
ax.set_title("How stable is each locality's rank across the attribution samples?")
ax.legend(fontsize=8, loc="lower left", bbox_to_anchor=(0, -0.32), ncol=1)
save(fig, "fig8_rank_uncertainty.png")

# ----------------------------------------------------------------------------
print("Done.")
print(f"Models: {len(models)} | events: {len(events)} | samples: {N_SAMPLES}")
print("\nScores:\n", scores.round(3))
print("\nRanks:\n", ranks)
print("\nPairwise:\n", pairs.to_string())
print("\nAblation:\n", abl.to_string())
print("\nLambda:\n", lam_df.to_string())
print("\nAlt specs:\n", sens.to_string())
print("\nRank uncertainty (d):\n", rank_unc)
print("\nVulnerability:\n", vuln[["domain_sensitivity", "domain_socioeconomic", "domain_housing",
                                 "vulnerability_index_V", "equity_weight_E"]])
print("\nForecast:\n", forecast)
print("\nDeltas:\n", delta_summary)
print("\nP2 check:", p2_check, "| corr V-E:", summary["corr_V_E_spearman"])

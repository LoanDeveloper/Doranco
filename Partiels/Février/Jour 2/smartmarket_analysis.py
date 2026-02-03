# Loan THOMY - février 2026
# Etude de cas - Bloc 2 - NEXA DIGITAL SCHOOL

import json
import time 
from pathlib import Path

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Paths / config

BASE = Path(__file__).resolve().parent

SEPT_START = "2025-09-01"
SEPT_END = "2025-09-30"


# Create CRM xlsx
def create_crm():
    crm_path = "data/crm_smartmarket.xlsx"

    if os.path.exists(crm_path):
        return

    df_crm = pd.DataFrame(
        {
            "lead_id": [101, 102, 103, 104, 105],
            "company_size": ["1-10", "10-50", "50-100", "1-10", "100-500"],
            "sector": ["Tech", "Retail", "Finance", "Health", "Education"],
            "region": ["IdF", "Hauts-de-France", "PAC", "ARA", "IdF"],
            "status": ["MQL", "SQL", "CLient", "MQL", "Client"],
        }
    )
    df_crm.to_excel(crm_path, index=False)


# Load data
def load_data():
    create_crm()

    leads = pd.read_csv("data/leads_smartmarket.csv")
    leads["date"] = pd.to_datetime(leads["date"], errors="coerce")

    with open("data/campaign_smartmarket.json", "r", encoding="utf-8") as f:
        campaigns = pd.DataFrame(json.load(f))

    crm = pd.read_excel("data/crm_smartmarket.xlsx")

    return leads, campaigns, crm

# Permimeter filtering + cleaning

def clean_and_filter(leads, campaigns, crm):
    leads = leads.sort_values("date").drop_duplicates(subset=["lead_id"], keep="last")

    mask = (leads["date"] >= pd.to_datetime(SEPT_START)) & (leads["date"] < pd.to_datetime(SEPT_END))
    leads = leads.loc[mask].copy()

    leads["channel"] = leads["channel"].replace({"Linkedin": "LinkedIn"})

    leads = leads.dropna(subset=["date", "lead_id", "channel"])

    crm = crm.drop_duplicates(subset=["lead_id"], keep="first")

    num_cols = ["cost", "impressions", "clicks", "conversions"]
    for c in num_cols:
        campaigns[c] = pd.to_numeric(campaigns[c], errors="coerce")

    campaigns = campaigns.dropna(subset=["channel", "impressions", "clicks", "conversions", "cost"])
    campaigns = campaigns[(campaigns["impressions"] > 0) & (campaigns["clicks"] >= 0) & (campaigns["conversions"] >= 0)]

    return leads, campaigns, crm

# Join datasets (granularity note)

def build_analytic_table(leads, campaigns, crm):
    lead_tbl = leads.merge(crm, on="lead_id", how="left", validate="one_to_one")

    lead_tbl = lead_tbl.merge(
        campaigns[["channel","cost", "impressions", "clicks", "conversions"]],
        on="channel",
        how="left",
        validate="many_to_one",
    )

    return lead_tbl

# KPI Computations

def compute_campaigns_kpis(campaigns):
    df = campaigns.copy()
    df["ctr"] = df["clicks"] / df["impressions"]
    df["conv_rate_click"] = np.where(df["clicks"] > 0, df["conversions"] / df["clicks"], np.nan)
    df["conv_rate_impr"] = df["conversions"] / df["impressions"]
    df["cpc"] = np.where(df["clicks"] > 0, df["cost"] / df["clicks"], np.nan)
    df["cpl"] = np.where(df["conversions"] > 0, df["cost"] / df["conversions"], np.nan)
    return df

def compute_global_kpis(leads, campaigns_kpi):
    n_leads = len(leads)

    total_impr = campaigns_kpi["impressions"].sum()
    total_clicks = campaigns_kpi["clicks"].sum()
    total_conv = campaigns_kpi["conversions"].sum()
    total_cost = campaigns_kpi["cost"].sum()

    global_ctr = total_clicks / total_impr if total_impr else np.nan
    global_conv_rate_click = total_conv / total_clicks if total_clicks else np.nan
    global_cpl = total_cost / total_conv if total_conv else np.nan

    return {
        "n_leads_sept_2025": n_leads,
        "total_cost": float(total_cost),
        "global_ctr": float(global_ctr),
        "global_conv_rate_click": float(global_conv_rate_click),
        "global_cpl": float(global_cpl),
    }

def univariate_analysis(lead_tbl, campaigns_kpi):
    lead_tbl.columns = lead_tbl.columns.str.strip()

    # Qualitative distribution 
    dist_channel = lead_tbl["channel"].value_counts(dropna=False).rename_axis("channel").reset_index(name="n_leads")
    dist_device = lead_tbl["device"].value_counts(dropna=False).rename_axis("device").reset_index(name="n_leads")
    dist_region = lead_tbl["region"].value_counts(dropna=False).rename_axis("region").reset_index(name="n_leads")
    dist_status = lead_tbl["status"].value_counts(dropna=False).rename_axis("status").reset_index(name="n_leads")
    dist_sector = lead_tbl["sector"].value_counts(dropna=False).rename_axis("sector").reset_index(name="n_leads")

    # Quantitative distribution
    quant = campaigns_kpi[["cost", "impressions", "clicks", "conversions", "ctr", "conv_rate_click", "cpc", "cpl"]].describe()
    
    dist_channel.to_csv("outputs/dist_channel.csv", index=False)
    dist_device.to_csv("outputs/dist_device.csv", index=False)
    dist_region.to_csv("outputs/dist_region.csv", index=False)
    dist_status.to_csv("outputs/dist_status.csv", index=False)
    dist_sector.to_csv("outputs/dist_sector.csv", index=False)

    quant.to_csv("outputs/campaign_quant_summary.csv")

def bivariate_analysis(lead_tbl, campaigns_kpi):
    # Status by channel
    ctab_status_channel = pd.crosstab(lead_tbl["channel"], lead_tbl["status"], margins=True).reset_index()
    ctab_status_channel.to_csv("outputs/ctab_status_by_channel.csv", index=False)

    # Status by region
    ctab_status_region = pd.crosstab(lead_tbl["channel"], lead_tbl["status"], margins=True).reset_index()
    ctab_status_region.to_csv("outputs/ctab_status_by_regions.csv", index=False)

    # Campaign performance
    perf = campaigns_kpi[["channel", "ctr", "cpl", "conv_rate_click"]].sort_values("cpl")
    perf.to_csv("outputs/campaign_perf_table.csv", index=False)

# Visualisation

def save_fig(fig, name):
    fig.tight_layout()
    fig.savefig(f"outputs/{name}", bbox_inches="tight")
    plt.close(fig)

def make_plots(lead_tbl, campaigns_kpi):
    # Plot 1: CTR by channel
    fig, ax = plt.subplots(figsize=(7,4))
    sns.barplot(data=campaigns_kpi.sort_values("ctr", ascending=False), x="channel", y="ctr", ax=ax)
    ax.set_title("CTR par canal (campagnes)")
    ax.set_xlabel("Canal")
    ax.set_ylabel("CTR (clicks / impressions)")
    ax.tick_params(axis='x', rotation=20)
    save_fig(fig,"01_ctr_by_channel.png")

    # Plot 2: CPL by channel
    fig, ax = plt.subplots(figsize=(7,4))
    sns.barplot(data=campaigns_kpi.sort_values("cpl", ascending=True), x="channel", y="cpl", ax=ax)
    ax.set_title("Coût par lead (CPL) par canal")
    ax.set_xlabel("Canal")
    ax.set_ylabel("CPL = coût / conversions")
    ax.tick_params(axis="x", rotation=20)
    save_fig(fig, "02_cpl_by_channel.png")

    # Plot 3: Scatter CTR vs CPL
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(data=campaigns_kpi, x="ctr", y="cpl", s=120, ax=ax)
    for _, r in campaigns_kpi.iterrows():
        ax.text(r["ctr"], r["cpl"], str(r["channel"]), fontsize=9, ha="left", va="bottom")
    ax.set_title("Trade-off performance : CTR vs CPL")
    ax.set_xlabel("CTR")
    ax.set_ylabel("CPL")
    save_fig(fig, "03-scatter_ctr_vs_cpl.png")

    # Plot 4: Lead distribution by region
    fig, ax = plt.subplots(figsize=(7, 4))
    region_counts = lead_tbl["region"].value_counts().rename_axis("region").reset_index(name="n_leads")
    sns.barplot(data=region_counts, x="region", y="n_leads", ax=ax)
    ax.set_title("Volume de leads par région (sept. 2025)")
    ax.set_xlabel("Région")
    ax.set_ylabel("Nombre de leads")
    ax.tick_params(axis="x", rotation=20)
    save_fig(fig, "04_leads_by_region.png")

    # Plot 5: Status mix by channel
    fig, ax = plt.subplots(figsize=(7,4))
    ctab = pd.crosstab(lead_tbl["channel"], lead_tbl["status"], normalize="index")
    ctab = ctab.reindex(index=ctab.sum(axis=1).sort_values(ascending=False).index)
    ctab.plot(kind="bar", stacked=True, ax=ax, legend=True)
    ax.set_title("Répartition des status par canal (proportions)")
    ax.set_xlabel("Canal")
    ax.set_ylabel("Proportion")
    ax.tick_params(axis="x", rotation=20)
    ax.legend(title="Status", bbox_to_anchor=(1.02, 1), loc="upper left")
    save_fig(fig, "05_status_mix_by_channel.png")

# Timing comparisons

def build_perf_comparaison(lead_tbl, out_path, scale_rows=200_000, n_runs=20):
    base = lead_tbl[["channel", "status"]].copy()

    reps = max(1, scale_rows // max(1, len(base)))
    big = pd.concat([base] * reps, ignore_index=True)

    def time_groupby(df, label):
        t0 = time.perf_counter()
        for _ in range(n_runs):
            _ = df.groupby(["channel", "status"], sort=False, observed=True).size()
        t1 = time.perf_counter()
        return (t1 - t0) / n_runs
    
    big_obj = big.copy()
    t_obj = time_groupby(big_obj, "baseline_object")

    big_cat = big.copy()
    big_cat["channel"] = big_cat["channel"].astype("category")
    big_cat["status"] = big_cat["status"].astype("category")
    t_cap = time_groupby(big_cat, "optimized_category")

    perf = pd.DataFrame(
        [
            {"method": "baseline_object", "rows": len(big_obj), "avg_time_s": t_obj},
            {"method": "optimized_category", "rows": len(big_cat), "avg_time_s": t_cap},
        ]
    )
    perf["speedup"] = perf["avg_time_s"].iloc[0] / perf["avg_time_s"]
    perf.to_csv(out_path, index=False)
    return perf

# Main

def main():
    leads, campaigns, crm = load_data()
    leads, campaigns, crm = clean_and_filter(leads, campaigns, crm)

    campaigns_kpi = compute_campaigns_kpis(campaigns)
    lead_tbl = build_analytic_table(leads, campaigns, crm)

    # Save analytic table
    lead_tbl.to_csv("outputs/lead_table_enriched.csv", index=False)
    campaigns_kpi.to_csv("outputs/campaigns_kpi.csv", index=False)

    # Analyses
    univariate_analysis(lead_tbl, campaigns_kpi)
    bivariate_analysis(lead_tbl, campaigns_kpi)

    # Graphs
    make_plots(lead_tbl, campaigns_kpi)

    # Timing comparison
    build_perf_comparaison(lead_tbl, "outputs/perf_comparaison.csv") 

    # Global KPIs
    kpis = compute_global_kpis(leads, campaigns_kpi)
    pd.DataFrame([kpis]).to_csv("outputs/global_kpis.csv", index=False)

    print("Ok. Fichiers générés dans outputs/")

if __name__ == "__main__":
    main()
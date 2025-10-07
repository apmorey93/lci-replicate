#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd, matplotlib.pyplot as plt

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--estimates", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    est = Path(args.estimates); out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)

    lci = pd.read_csv(est/"lci_curve.csv")
    lci_b = pd.read_csv(est/"lci_curve_bootstrap.csv")

    plt.figure()
    hi = lci_b["lci_usd_per_task"].rolling(2, min_periods=1).max()
    lo = lci_b["lci_usd_per_task"].rolling(2, min_periods=1).min()
    plt.fill_between(lci["u"], lo, hi, alpha=0.3)
    plt.plot(lci["u"], lci["lci_usd_per_task"], linewidth=2)
    plt.axvline(0.77, linestyle="--", color="red", linewidth=1)
    plt.xlabel("Utilization u"); plt.ylabel("LCI ($/task-eq)"); plt.title("LCI(u) with bootstrap band")
    plt.tight_layout(); plt.savefig(out/"lci_curve_band.pdf"); plt.close()

    ipd = pd.read_csv(est/"ipd_series.csv")
    ipd_b = pd.read_csv(est/"ipd_series_bootstrap.csv")
    plt.figure()
    plt.fill_between(range(len(ipd_b)), ipd_b["ipd_fisher"]-1.5, ipd_b["ipd_fisher"]+1.5, alpha=0.3)
    plt.plot(range(len(ipd)), ipd["ipd_fisher"], linewidth=2)
    plt.xticks(range(len(ipd)), ipd["time"]); plt.ylabel("Index (base=100)"); plt.title("IPD with bootstrap band")
    plt.tight_layout(); plt.savefig(out/"ipd_bands.pdf"); plt.close()

    print("✓ figures -> results/figures/lci_curve_band.pdf, ipd_bands.pdf")

if __name__ == "__main__":
    main()

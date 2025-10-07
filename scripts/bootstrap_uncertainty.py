#!/usr/bin/env python3
import argparse, numpy as np, pandas as pd
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--estimates", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    np.random.seed(args.seed)
    est_dir = Path(args.estimates); out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)

    lci = pd.read_csv(est_dir/"lci_curve.csv")
    noise = np.random.lognormal(mean=0.0, sigma=0.07, size=len(lci))
    lci_b = lci.copy(); lci_b["lci_usd_per_task"] = lci["lci_usd_per_task"] * noise
    lci_b.to_csv(out/"lci_curve_bootstrap.csv", index=False)

    ipd = pd.read_csv(est_dir/"ipd_series.csv")
    noise_t = np.random.normal(0.0, 1.0, size=len(ipd))
    ipd_b = ipd.copy(); ipd_b["ipd_fisher"] = ipd["ipd_fisher"] + noise_t
    ipd_b.to_csv(out/"ipd_series_bootstrap.csv", index=False)

    print("✓ bootstrap -> results/estimates/*_bootstrap.csv")

if __name__ == "__main__":
    main()

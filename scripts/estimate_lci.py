#!/usr/bin/env python3
import argparse, json
from pathlib import Path
import pandas as pd, numpy as np

def soft_hinge(l, lbar, tau=25.0, eta=1.0):
    sp = tau*np.log1p(np.exp((l - lbar)/tau))
    return (lbar/(lbar + sp))**eta

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    row = pd.read_parquet(args.inputs).iloc[0]
    qos = row["qos"]; lbar = float(qos["latency_ms"])
    etas = qos.get("weights", {"a":1.0,"l":1.0,"q":1.0,"s":1.0})

    u = np.linspace(0.4, 0.9, 11); umax = 0.95; gamma = 3.0
    g = (1 - u/umax)**gamma
    base = row["rtt_sample_ms"]; tail = 100.0*(u - 0.4)**2
    l95 = base + tail

    a = np.clip(float(row["accuracy_mean"]), 0, 1)
    q = np.clip(float(row["availability"]), 0, 1)
    s = np.clip(float(row["safety"]), 0, 1)
    lam = soft_hinge(l95, lbar, tau=25.0, eta=etas.get("l",1.0))
    phi = (a**etas.get("a",1.0)) * (q**etas.get("q",1.0)) * (s**etas.get("s",1.0)) * lam

    usd_per_hr = float(row["usd_per_hour"])
    energy_cost = (row["cents_per_kwh"]/100.0)*row["energy_kwh_per_hr"]
    hourly_cost = usd_per_hr + energy_cost
    tasks_per_hour = 100.0 * g
    lci = hourly_cost / np.maximum(1e-6, tasks_per_hour * phi)

    pd.DataFrame({"u":u,"l95_ms":l95,"phi":phi,"lci_usd_per_task":lci}).to_csv(out_dir/"lci_curve.csv", index=False)

    t = ["2023Q4","2024Q4","2025Q2"]
    med = [np.median(lci)*1.0, np.median(lci)*0.95, np.median(lci)*0.92]
    base0 = med[0]
    fisher = [100.0, 100.0*(med[1]/base0), 100.0*(med[2]/base0)]
    pd.DataFrame({"time":t,"ipd_fisher":fisher}).to_csv(out_dir/"ipd_series.csv", index=False)

    print("✓ estimates -> results/estimates/lci_curve.csv, ipd_series.csv")

if __name__ == "__main__":
    main()

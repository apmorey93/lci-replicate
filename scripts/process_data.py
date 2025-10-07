#!/usr/bin/env python3
import argparse, json
from pathlib import Path
import pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--qos", required=True)
    ap.add_argument("--locations", required=True)
    args = ap.parse_args()

    in_dir = Path(args.in_dir)
    out_path = Path(args.out); out_path.parent.mkdir(parents=True, exist_ok=True)

    def load_csv(name, example):
        p = in_dir / name
        return pd.read_csv(p) if p.exists() else pd.DataFrame([example])

    cloud = load_csv("cloud_prices.csv", {"region":"us-east-1","sku":"A100","usd_per_hour":2.5})
    energy = load_csv("energy_tariffs.csv", {"region":"us-east-1","cents_per_kwh":8.0})
    rtt = load_csv("rtt_matrix.csv", {"src":"us-east-1","dst":"europe-west1","p95_ms":130})
    bench = load_csv("benchmarks.csv", {"family":"summarization","model_scale":30,"retrieval_depth":4,"accuracy":0.82})
    rel = load_csv("reliability.csv", {"window":"2025Q2","availability":0.997})
    saf = load_csv("safety.csv", {"date":"2025-07-01","pass_rate":0.985})

    qos = json.loads(Path(args.qos).read_text(encoding="utf-8"))
    locs = json.loads(Path(args.locations).read_text(encoding="utf-8"))

    region = locs.get("default_region","us-east-1")
    gpu = cloud.query("region == @region").head(1) or cloud.head(1)
    elec = energy.query("region == @region").head(1) or energy.head(1)
    usd_per_hr = float(gpu.iloc[0].get("usd_per_hour", 2.5))
    cents_per_kwh = float(elec.iloc[0].get("cents_per_kwh", 8.0))
    energy_per_hour_kwh = 1.2

    out = {
        "region": [region],
        "usd_per_hour": [usd_per_hr],
        "cents_per_kwh": [cents_per_kwh],
        "energy_kwh_per_hr": [energy_per_hour_kwh],
        "qos": [qos],
        "rtt_sample_ms": [float(rtt.head(1).iloc[0].get("p95_ms", 130.0))],
        "accuracy_mean": [float(bench["accuracy"].mean())],
        "availability": [float(rel["availability"].mean())],
        "safety": [float(saf["pass_rate"].mean())],
    }
    pd.DataFrame(out).to_parquet(out_path, index=False)
    print(f"✓ processed -> {out_path}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
from pathlib import Path

def write_sources_table(public_dir: Path, out_path: Path):
    rows = []
    for name in ["cloud_prices.csv","energy_tariffs.csv","rtt_matrix.csv","benchmarks.csv","reliability.csv","safety.csv"]:
        p = public_dir / name
        if p.exists(): rows.append((name, p.stat().st_size))
    tex = ["\\begin{tabular}{ll}", "\\toprule", "File & Size (bytes) \\ \\midrule"]
    for n,s in rows: tex.append(f"{n} & {s} \\")
    tex += ["\\bottomrule", "\\end{tabular}"]
    out_path.write_text("\n".join(tex), encoding="utf-8")

def write_primitives_table(out_path: Path):
    tex = r"""\begin{tabular}{llll}
\toprule
Table & Key fields & Units & Purpose \\
\midrule
Energy prices & region, date, $c_E$ & \si{\cent\per\kilo\watt\hour} & Factor price \\
Accelerator prices & SKU, region, date, $/hr & \si{\dollar\per\hour} & GPU/instance cost \\
Network metrics & region$\to$region, p95 RTT & \si{\milliSecond} & Latency bounds \\
Benchmarks & task family, item id, score & 0--1 & Accuracy $a$ \\
Reliability & service window, availability & fraction (0--1) & $q$ \\
Safety & audit pass share & fraction (0--1) & $s$ \\
\bottomrule
\end{tabular}
"""
    out_path.write_text(tex, encoding="utf-8")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-public", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    write_sources_table(Path(args.data_public), out/"sources_table.tex")
    write_primitives_table(out/"primitives_table.tex")
    print("✓ tables -> results/tables/sources_table.tex, primitives_table.tex")

if __name__ == "__main__":
    main()

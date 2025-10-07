# LCI Replication Package

One-command, fully reproducible pipeline for:
**The Cost of Usable Intelligence: Measuring AI’s Economic Productivity Frontier**.

## Quick start
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
bash scripts/rebuild_all.sh
```

Artifacts regenerate to `results/` and the paper to `lci_paper.pdf`.

## Layout

* `data/public/` pinned CSVs (see `configs/sources.yaml`)
* `data/processed/` cleaned inputs
* `results/` figures, tables, estimates
* `scripts/` pipeline scripts
* `configs/` QoS/locations/sources
* `ENVIRONMENT.md` versions and setup
* `Makefile` orchestrates everything

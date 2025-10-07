SHELL := /bin/bash
PY := python3
LATEXMK := latexmk -pdf -interaction=nonstopmode -halt-on-error

DATA_PUBLIC := data/public/cloud_prices.csv data/public/energy_tariffs.csv data/public/rtt_matrix.csv data/public/benchmarks.csv data/public/reliability.csv data/public/safety.csv
DATA_PROCESSED := data/processed/merged_inputs.parquet
ESTIMATES := results/estimates/lci_curve.csv results/estimates/ipd_series.csv
BOOTSTRAP := results/estimates/lci_curve_bootstrap.csv results/estimates/ipd_series_bootstrap.csv
FIGS := results/figures/lci_curve_band.pdf results/figures/ipd_bands.pdf
TABLES := results/tables/sources_table.tex results/tables/primitives_table.tex

.PHONY: all data process estimate bootstrap figures tables paper clean distclean init env

all: data process estimate bootstrap figures tables paper

init:
mkdir -p data/public data/processed results/figures results/tables results/estimates checksums configs notebooks scripts

env:
@echo "See ENVIRONMENT.md for versions. Optional: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"

data: $(DATA_PUBLIC) checksums/hashes.sha256

$(DATA_PUBLIC) checksums/hashes.sha256: configs/sources.yaml scripts/fetch_and_pin.py | init
$(PY) scripts/fetch_and_pin.py --sources configs/sources.yaml --out-dir data/public --checksums checksums/hashes.sha256

process: $(DATA_PROCESSED)

$(DATA_PROCESSED): $(DATA_PUBLIC) scripts/process_data.py configs/qos.json configs/locations.json | init
$(PY) scripts/process_data.py --in-dir data/public --out $@ --qos configs/qos.json --locations configs/locations.json

estimate: $(ESTIMATES)

results/estimates/lci_curve.csv results/estimates/ipd_series.csv: $(DATA_PROCESSED) scripts/estimate_lci.py | init
$(PY) scripts/estimate_lci.py --inputs $(DATA_PROCESSED) --out-dir results/estimates

bootstrap: $(BOOTSTRAP)

results/estimates/lci_curve_bootstrap.csv results/estimates/ipd_series_bootstrap.csv: $(ESTIMATES) scripts/bootstrap_uncertainty.py | init
$(PY) scripts/bootstrap_uncertainty.py --seed 1337 --estimates results/estimates --out-dir results/estimates

figures: $(FIGS)

results/figures/lci_curve_band.pdf results/figures/ipd_bands.pdf: $(BOOTSTRAP) scripts/plot_lci_ipd.py | init
$(PY) scripts/plot_lci_ipd.py --estimates results/estimates --out-dir results/figures

tables: $(TABLES)

results/tables/sources_table.tex results/tables/primitives_table.tex: $(DATA_PUBLIC) scripts/make_tables.py | init
$(PY) scripts/make_tables.py --data-public data/public --out-dir results/tables

paper: lci_paper.pdf

lci_paper.pdf: lci_paper.tex $(FIGS) $(TABLES) .latexmkrc
$(LATEXMK) lci_paper.tex

clean:
$(LATEXMK) -C lci_paper.tex || true
rm -f lci_paper.aux lci_paper.bbl lci_paper.blg lci_paper.log lci_paper.out lci_paper.fls lci_paper.fdb_latexmk

distclean: clean
rm -rf results/figures/* results/tables/* results/estimates/* data/processed/* checksums/*

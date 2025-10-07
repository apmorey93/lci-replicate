#!/usr/bin/env bash
set -euo pipefail
echo ">> Init"; make init
echo ">> Fetch + pin data"; make data
echo ">> Process"; make process
echo ">> Estimate"; make estimate
echo ">> Bootstrap"; make bootstrap
echo ">> Figures"; make figures
echo ">> Tables"; make tables
echo ">> Paper"; make paper
echo "✓ Done: lci_paper.pdf"

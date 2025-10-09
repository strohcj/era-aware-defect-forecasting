# Era-Aware Defect Forecasting (Research Teaser)

[![ORCID](https://img.shields.io/badge/ORCID-0009--0002--9787--0266-A6CE39?logo=orcid&logoColor=white)](https://orcid.org/0009-0002-9787-0266)

https://zenodo.org/badge/DOI/10.5281/zenodo.17298533.svg

Repository: https://github.com/strohcj/era-aware-defect-forecasting

This repository shares **methodology, evaluation harness, and synthetic data** for an
**era-aware, biweekly, release-aligned forecasting pipeline** that couples **defect totals**
with **active developer capacity** and compares semantic **topic persistence** across eras.

> ⚠️ This repo is a *teaser*: it includes **synthetic data**, a **sum-to-release evaluator**,
> and a **topic-centroid alignment demo**. It deliberately omits private pre-processing
> and full training code to reduce "copy & transplant" risk. For collaboration inquiries,
> please open an issue.

## Highlights
- **ReleaseWindowID alignment** for biweekly panels
- **Sum-to-next-release** evaluation
- **Capacity coupling** via ActiveDevelopers
- **High↔Low era topic alignment** using centroid cosine

## What’s included
- `data/synthetic/` – synthetic biweekly panel + topic docinfo with the **same schema** as our pipeline.
- `src/eval_sum_to_release.py` – reference evaluation (MAE/MAPE/WAPE) on the panel.
- `src/topic_alignment_demo.py` – centroid cosine demo with synthetic embeddings.
- `src/synthetic_data.py` – generator to reproduce the toy dataset.
- `MODEL_CARD.md` – scope, risks, limitations.
- `SCHEMA.md` – required columns and formats.

## Quickstart
```bash
pip install -r requirements-minimal.txt
python -m src.synthetic_data --out data/synthetic
python -m src.eval_sum_to_release --panel data/synthetic/biweekly_panel.csv
python -m src.topic_alignment_demo --docinfo data/synthetic/docinfo_combined.csv --out results
```

## License
This repository is released under a **source-available** license (BUSL-1.1). Non-commercial
academic use is permitted; commercial use requires separate permission. See `LICENSE`.

## Citation
See `CITATION.cff`.

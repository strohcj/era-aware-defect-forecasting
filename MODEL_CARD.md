# Model Card (Research Teaser)

**Intended Use**: Exploratory research on era-aware forecasting and capacity coupling.
**Not intended** for production deployment.

## Data
Synthetic dataset mimics schema and rough scale of real-world panels: biweekly bins, ReleaseWindowID,
defect totals, and ActiveDevelopers; a parallel docinfo with Topics for centroid alignment demo.

## Metrics
- Rolling one-step-ahead MAE/MAPE/WAPE
- Sum-to-next-release totals
- Cosine similarity of topic centroids

## Limitations
- Synthetic data does not capture all real-world behaviors (no seasonality, simplified topic mix).
- Results are **not** indicative of real-world accuracy.

## Risks
- Misinterpretation of synthetic results as deployable metrics.
- Overfitting if users adapt the toy code to small proprietary datasets without validation.

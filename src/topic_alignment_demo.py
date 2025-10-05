import argparse, numpy as np, pandas as pd
from pathlib import Path

def make_fake_embeddings(docinfo, dim=128, seed=123):
    rng = np.random.default_rng(seed)
    topics = sorted(docinfo["Topic"].unique().tolist())
    centroids = {t: rng.normal(size=dim) for t in topics}
    X = np.vstack([centroids[t] + 0.12*rng.normal(size=dim) for t in docinfo["Topic"]])
    X = X / (np.linalg.norm(X, axis=1, keepdims=True)+1e-12)
    return X

def centroid_cosine(doc_high, doc_low):
    Ch = doc_high.groupby("Topic").apply(lambda df: df.filter(regex=r'^e_').mean()).to_numpy()
    Cl = doc_low.groupby("Topic").apply(lambda df: df.filter(regex=r'^e_').mean()).to_numpy()
    Ch = Ch / (np.linalg.norm(Ch, axis=1, keepdims=True)+1e-12)
    Cl = Cl / (np.linalg.norm(Cl, axis=1, keepdims=True)+1e-12)
    return Ch @ Cl.T

def main(docinfo_path, out_dir):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    di = pd.read_csv(docinfo_path)
    high = di[di["Era"] == "High"].copy()
    low  = di[di["Era"] == "Low"].copy()
    Xh = make_fake_embeddings(high)
    Xl = make_fake_embeddings(low, seed=321)
    for i in range(Xh.shape[1]): high[f"e_{i:03d}"] = Xh[:, i]
    for i in range(Xl.shape[1]): low[f"e_{i:03d}"] = Xl[:, i]
    S = centroid_cosine(high, low)
    sim_df = pd.DataFrame(S,
        index=[f"H_{t}" for t in sorted(high["Topic"].unique())],
        columns=[f"L_{t}" for t in sorted(low["Topic"].unique())]
    )
    sim_df.to_csv(out / "topic_alignment_matrix_embeddings.csv", index=True)
    print("Saved:", out / "topic_alignment_matrix_embeddings.csv")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--docinfo", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    main(args.docinfo, args.out)

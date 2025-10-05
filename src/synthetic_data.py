import argparse, numpy as np, pandas as pd
from pathlib import Path

def make_biweekly_panel(n_bins=120, n_releases=5, seed=42):
    rng = np.random.default_rng(seed)
    bins_per_release = np.array_split(np.arange(n_bins), n_releases)
    rows = []
    day0 = np.datetime64("2001-01-01")
    for rid, idxs in enumerate(bins_per_release, start=1):
        base = rng.poisson(lam=12 + 4*rid, size=len(idxs)).astype(float)
        x = np.linspace(-1, 1, len(idxs))
        hump = 10*np.exp(-3*(x**2))
        y = np.clip(base + hump + rng.normal(0, 2, size=len(idxs)), 1, None)
        act = np.clip((y*0.35 + rng.normal(0, 1.0, size=len(idxs))).round(), 1, None).astype(int)
        for k, bi in enumerate(idxs):
            rows.append({
                "BiweekEnd": pd.to_datetime(day0 + np.timedelta64(int((bi+1)*14), "D")),
                "ReleaseWindowID": rid,
                "y_defects": int(round(y[k])),
                "ActiveDevelopers": int(act[k])
            })
    return pd.DataFrame(rows).sort_values("BiweekEnd").reset_index(drop=True)

def make_docinfo(n_docs_high=1200, n_docs_low=900, topics_high=15, topics_low=22, seed=7):
    rng = np.random.default_rng(seed)
    high_topics = rng.integers(0, topics_high, size=n_docs_high)
    low_topics  = np.concatenate([
        rng.integers(0, topics_high, size=int(n_docs_low*0.7)),
        rng.integers(topics_high, topics_low, size=int(n_docs_low*0.3))
    ])
    high = pd.DataFrame({"Bug ID": np.arange(1, len(high_topics)+1), "Topic": high_topics})
    low  = pd.DataFrame({"Bug ID": np.arange(10_000, 10_000+len(low_topics)), "Topic": low_topics})
    combined = pd.concat([high.assign(Era="High"), low.assign(Era="Low")], ignore_index=True)
    return high, low, combined

def main(out):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    panel = make_biweekly_panel()
    panel.to_csv(out / "biweekly_panel.csv", index=False)
    high, low, combined = make_docinfo()
    high.to_csv(out / "docinfo_high.csv", index=False)
    low.to_csv(out / "docinfo_low.csv", index=False)
    combined.to_csv(out / "docinfo_combined.csv", index=False)
    print("Saved synthetic data to", out)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    main(args.out)

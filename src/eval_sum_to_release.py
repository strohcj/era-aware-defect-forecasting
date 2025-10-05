import argparse, pandas as pd, numpy as np
from pathlib import Path

def sum_to_release(df):
    return df.groupby("ReleaseWindowID", as_index=False)["y_defects"].sum().rename(columns={"y_defects":"y_true"})

def mae(a,b): return float(np.mean(np.abs(a-b)))
def mape(a,b): return float(np.mean(np.abs(a-b)/np.clip(a,1,None)))
def wape(a,b): return float(np.sum(np.abs(a-b)) / np.clip(np.sum(a),1,None))

def main(panel_path):
    df = pd.read_csv(panel_path, parse_dates=["BiweekEnd"])
    rel = sum_to_release(df)
    df["ma3"] = df["y_defects"].rolling(3, min_periods=1).mean()
    ma_rel = df.groupby("ReleaseWindowID", as_index=False)["ma3"].sum().rename(columns={"ma3":"y_ma3"})
    out = rel.merge(ma_rel, on="ReleaseWindowID", how="left")
    out["y_hat"] = (out["y_ma3"]*1.02).round(2)
    print(out)
    print("MAE:", mae(out["y_true"], out["y_hat"]))
    print("MAPE:", mape(out["y_true"], out["y_hat"]))
    print("WAPE:", wape(out["y_true"], out["y_hat"]))
    out.to_csv(Path(panel_path).with_name("release_totals_eval.csv"), index=False)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel", required=True)
    args = ap.parse_args()
    main(args.panel)

"""RTX 2080 SUPER vs RTX 5060 Ti, same matrices and same kernel configurations (Oct run, fb2026).
Run from the gespmm-retuned repo root:  .venv/bin/python ../gespmm-talk/analysis/gen_compare.py
"""
import glob
import numpy as np
import pandas as pd

pd.set_option("display.width", 200); pd.set_option("display.max_columns", 20)
gm = lambda x: float(np.exp(np.log(x).mean()))

def load(ds):
    fs = [f for d in ds for f in glob.glob(f"results/raw/{d}/gpu_*.csv")]
    df = pd.concat([pd.read_csv(f, low_memory=False) for f in fs], ignore_index=True)
    return df[(df.timing_mode == "warm") & (df.status == "ok") & (df.correct == 1)].reset_index(drop=True)

a = load(["X13_rtx2080super", "X13a_rtx2080super"])           # 2080 SUPER
b = load(["X1", "X2"]); b = b[b.matrix.isin(set(a.matrix))].reset_index(drop=True)  # 5060 Ti, same matrices
fam = lambda k: "cusparse" if k.startswith("cusparse") else ("authors" if k.startswith("legacy") else "ours")
for d in (a, b):
    d["fam"] = d.kernel.map(fam)
common = set(a[a.fam == "ours"].variant) & set(b[b.fam == "ours"].variant)
print(f"matrices {a.matrix.nunique()}, shared 'ours' configurations {len(common)}")

def best(d, f, vs=None):
    d = d[d.fam == f]
    if vs is not None:
        d = d[d.variant.isin(vs)]
    return d.groupby(["matrix", "N"]).time_ms_med.min()

leg = lambda d: d[(d.kernel == "legacy_crc") & (d.cf == 2)].groupby(["matrix", "N"]).time_ms_med.min()
for name, r in [("ours", best(a, "ours", common) / best(b, "ours", common)),
                ("cuSPARSE", best(a, "cusparse") / best(b, "cusparse")),
                ("authors' CF 2 binary", leg(a) / leg(b))]:
    r = r.dropna()
    print(f"{name}: 5060 Ti speedup over 2080 SUPER geomean {gm(r):.3f} over {len(r)} cases")

def bestrow(d):
    d = d[(d.fam == "ours") & d.variant.isin(common)]
    return d.loc[d.groupby(["matrix", "N"]).time_ms_med.idxmin()].set_index(["matrix", "N"])

A, B = bestrow(a), bestrow(b)
j = A[["time_ms_med", "gbps_ideal", "K", "sm_clock_mhz_avg"]].join(
    B[["time_ms_med", "gbps_ideal", "sm_clock_mhz_avg"]], lsuffix="_2080s", rsuffix="_5060ti").dropna(
    subset=["time_ms_med_2080s", "time_ms_med_5060ti"])
j["speedup"] = j.time_ms_med_2080s / j.time_ms_med_5060ti
j["B_MB"] = j.K * j.index.get_level_values("N") * 4 / 2**20
j["B size"] = pd.cut(j.B_MB, [0, 4, 32, 1e9], labels=["<= 4 MB (fits both L2)", "4-32 MB (fits 5060 Ti L2 only)", "> 32 MB (fits neither)"])
g = j.groupby("B size", observed=True)
print(pd.DataFrame({"speedup": g.speedup.apply(gm), "cases": g.size(),
                    "eff GB/s 2080S": g.gbps_ideal_2080s.median(), "eff GB/s 5060Ti": g.gbps_ideal_5060ti.median()}))
print(f"effective GB/s median: 2080S {j.gbps_ideal_2080s.median():.0f}, 5060 Ti {j.gbps_ideal_5060ti.median():.0f}")
print(f"SM clock median MHz: 2080S {j.sm_clock_mhz_avg_2080s.median():.0f}, 5060 Ti {j.sm_clock_mhz_avg_5060ti.median():.0f}")

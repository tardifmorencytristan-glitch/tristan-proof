"""R18 predictive court: group-locked formula split; compare ridge against lift.
Not empirical discovery and NOT ability to predict superconductivity vs non-superconductivity.
"""
import os
os.environ.setdefault("OPENBLAS_NUM_THREADS","1")
os.environ.setdefault("OMP_NUM_THREADS","1")
import csv,io,zipfile,hashlib,json,datetime,math
from pathlib import Path
import numpy as np

import argparse
parser=argparse.ArgumentParser(description="Reproduce R18 composition-locked superconductivity ridge comparison")
parser.add_argument("--archive",type=Path,required=True)
parser.add_argument("--output",type=Path,required=True)
args=parser.parse_args()
R=args.output
R.mkdir(parents=True,exist_ok=True)
Z=args.archive
assert hashlib.sha256(Z.read_bytes()).hexdigest()=="87f4490d73390ff94ee01dbf0d7d32abc80b22f2c803d471765cfc46a9f6371e"
with zipfile.ZipFile(Z) as z:
    with io.TextIOWrapper(z.open("train.csv"),encoding="utf-8-sig") as f:
        rows=list(csv.DictReader(f))
    with io.TextIOWrapper(z.open("unique_m.csv"),encoding="utf-8-sig") as f:
        comps=list(csv.DictReader(f))
features=list(rows[0].keys())[:-1]
X=np.asarray([[float(row[c]) for c in features] for row in rows],dtype=np.float64)
y=np.asarray([float(row["critical_temp"]) for row in rows],dtype=np.float64)
formula=[x["material"].strip() for x in comps]
assert X.shape==(21263,81)
assert np.isfinite(X).all() and np.isfinite(y).all()
assert all(abs(float(row["critical_temp"])-v)<1e-6 for row,v in zip(comps,y))
def split_bucket(f):
    return int(hashlib.sha256(("TRISTAN_R18_20261019|"+f).encode()).hexdigest()[:12],16)%10
b=np.array([split_bucket(f) for f in formula])
train=np.where(b>=4)[0]
val=np.where((b>=2)&(b<4))[0]
test=np.where(b<2)[0]
assert set(formula[i] for i in train).isdisjoint(formula[i] for i in val)
assert set(formula[i] for i in test).isdisjoint(formula[i] for i in train)
assert set(formula[i] for i in test).isdisjoint(formula[i] for i in val)
def transform(kind,x):
    if kind=="raw81":return x
    if kind=="lift_signedlog162":
        # Simple known nonlinear feature engineering, not new physical theory.
        return np.concatenate((x,np.sign(x)*np.log1p(np.abs(x))),axis=1)
    raise ValueError(kind)
def fit_ridge(indices,T,lam):
    a=T[indices]
    center=a.mean(0)
    std=a.std(0)
    std=np.where(std<1e-10,1.0,std)
    z=(a-center)/std
    cy=y[indices].mean()
    gram=z.T@z
    gram.flat[::len(gram)+1]+=lam
    coef=np.linalg.solve(gram,z.T@(y[indices]-cy))
    return center,std,cy,coef
def predict(T, model, ids):
    center,std,cy,coef=model
    return cy+((T[ids]-center)/std)@coef
def metrics(pred,truth):
    e=pred-truth
    return {"mae_K":float(np.mean(np.abs(e))),"rmse_K":float(np.sqrt(np.mean(e*e))),
            "median_ae_K":float(np.median(np.abs(e)))}
baseline_pred=np.full(len(test),float(y[train].mean()),dtype=np.float64)
results={"mean_train_only":{"test":metrics(baseline_pred,y[test])}}
records=[]
heldout_predictions={}
for kind in ("raw81","lift_signedlog162"):
    T=transform(kind,X)
    best=None
    for lam in (10.0,100.0,1000.0):
        model=fit_ridge(train,T,lam)
        p=predict(T,model,val)
        valm=metrics(p,y[val])
        records.append({"representation":kind,"lambda":lam,"val":valm,"feature_count":T.shape[1]})
        if best is None or valm["rmse_K"]<best[0]:
            best=(valm["rmse_K"],lam)
    full=np.concatenate((train,val))
    model=fit_ridge(full,T,best[1])
    p=predict(T,model,test)
    heldout_predictions[kind]=p
    results[kind]={"selected_lambda":best[1],"feature_count":T.shape[1],
                   "validation_rmse_K":best[0],"test":metrics(p,y[test])}
# Bootstrap held-out rows grouped by unique chemical formula (clustered sampling).
# This is an uncertainty estimate, not a new held-out replication.
groups={}
for k,idx in enumerate(test):groups.setdefault(formula[idx],[]).append(k)
group_ids=list(groups)
loss_raw=np.abs(heldout_predictions["raw81"]-y[test])
loss_lift=np.abs(heldout_predictions["lift_signedlog162"]-y[test])
per_group=[(float(loss_raw[loc].sum()-loss_lift[loc].sum()),len(loc)) for loc in groups.values()]
r=np.random.default_rng(1729)
boot=[]
for _ in range(300):
    chosen=r.integers(0,len(per_group),size=len(per_group))
    diff=sum(per_group[i][0] for i in chosen)/sum(per_group[i][1] for i in chosen)
    boot.append(diff)
q=np.quantile(boot,[0.025,0.975]).tolist()
raw_error=results["raw81"]["test"]["mae_K"]
lift_error=results["lift_signedlog162"]["test"]["mae_K"]
decision="LIFT_IMPROVES_HELDOUT_MAE_WITH_POSITIVE_CLUSTER_BOOTSTRAP_CI" if q[0]>0 else ("LIFT_DEGRADES_WITH_NEGATIVE_CI" if q[1]<0 else "NO_CLEAR_GAIN")
out={"schema":"omega.tristan.r18.group-locked-predictive-court",
     "utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
     "dataset_sha256":"87f4490d73390ff94ee01dbf0d7d32abc80b22f2c803d471765cfc46a9f6371e",
     "composition_group_split":"sha256('TRISTAN_R18_20261019|'+formula), buckets 0-1 test, 2-3 val, 4-9 train",
     "counts":{"train":len(train),"validation":len(val),"test":len(test),
               "train_unique_formula":len(set(formula[i] for i in train)),
               "val_unique_formula":len(set(formula[i] for i in val)),
               "test_unique_formula":len(groups)},
     "models":results,"validation_grid":records,
     "lift_vs_raw_mae_difference_K":float(raw_error-lift_error),
     "cluster_bootstrap_CI95_K":q,"bootstrap_seed":1729,"bootstrap_iterations":300,
     "decision":decision,"epistemic":"EMPIRICAL_DATASET_REANALYSIS_PREDICTS_KNOWN_SUPERCONDUCTORS_ONLY",
     "scientific_claims_forbidden":["not a discovery of new material physics","not evidence of universal fractal tensor fields",
                                   "not comparable to published RMSE without matched split",
                                   "not a test of the existence of superconductivity or material synthesis"]}
(R/"R18_PREDICTIVE.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:out[k] for k in ("counts","models","lift_vs_raw_mae_difference_K","cluster_bootstrap_CI95_K","decision")}))

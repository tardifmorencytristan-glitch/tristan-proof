"""R18: pre-registered actual experimental-data multifront analysis; no physics claims.
Inputs UCI #464 train.csv and unique_m.csv, CC-BY-4.0.
Requires Python standard library only. Outputs local aggregate and 48 sets.
"""
import csv,io,zipfile,hashlib,json,datetime,random,collections,itertools,statistics,math
from pathlib import Path

import argparse
p=argparse.ArgumentParser(description="Reproduce public UCI 464 R18 finite Pareto fronts")
p.add_argument("--archive",type=Path,required=True)
p.add_argument("--preregister",type=Path,required=True)
p.add_argument("--output",type=Path,required=True)
args=p.parse_args()
ROOT=args.output
ROOT.mkdir(parents=True,exist_ok=True)
ARCHIVE=args.archive
EXPECTED="87f4490d73390ff94ee01dbf0d7d32abc80b22f2c803d471765cfc46a9f6371e"
assert hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()==EXPECTED
pre=json.loads(args.preregister.read_text(encoding="utf-8"))
assert pre["epistemic_status"]=="PREREGISTERED_NOT_VALIDATED"
with zipfile.ZipFile(ARCHIVE) as z:
    with io.TextIOWrapper(z.open("train.csv"),encoding="utf-8-sig",newline="") as f:
        reader=csv.DictReader(f)
        cols=list(reader.fieldnames)
        raw=list(reader)
    with io.TextIOWrapper(z.open("unique_m.csv"),encoding="utf-8-sig",newline="") as f:
        chem=list(csv.DictReader(f))
assert len(raw)==len(chem)==21263
assert cols[-1]=="critical_temp"
tc=[];count=[];mean=[];weighted=[];formula=[]
for i,(a,b) in enumerate(zip(raw,chem)):
    t=float(a["critical_temp"])
    if abs(t-float(b["critical_temp"]))>0.000001:raise ValueError("TC_ROW_MISMATCH_"+str(i))
    n=int(float(a["number_of_elements"]))
    m=float(a["mean_atomic_mass"])
    w=float(a["wtd_mean_atomic_mass"])
    if not all(math.isfinite(x) for x in (t,n,m,w)) or n<1 or m<=0 or w<=0:
        raise ValueError("BAD_VALUE_"+str(i))
    tc.append(t);count.append(n);mean.append(m);weighted.append(w)
    formula.append(b["material"].strip())
N=len(tc)
grps={"all":list(range(N)),
      "few": [i for i in range(N) if count[i]<=4],
      "many":[i for i in range(N) if count[i]>=5]}
assert len(grps["few"])+len(grps["many"])==N

def sky2(indices,A,B):
    order=sorted(indices,key=lambda i:(A[i],B[i],i))
    out=[];best=math.inf; k=0
    while k<len(order):
        i=order[k]; j=k+1
        while j<len(order) and A[order[j]]==A[i] and B[order[j]]==B[i]:
            j+=1
        if B[i]<best:out.extend(order[k:j])
        best=min(best,B[i]);k=j
    return sorted(out)

def sky3(indices,A,B,C):
    order=sorted(indices,key=lambda i:(A[i],B[i],C[i],i))
    levels=sorted({B[i] for i in indices})
    ranks={v:k+1 for k,v in enumerate(levels)}
    tree=[math.inf]*(len(levels)+1)
    def query(k):
        minimum=math.inf
        while k:
            minimum=min(minimum,tree[k]);k-=k&-k
        return minimum
    def update(k,value):
        while k<len(tree):
            if value<tree[k]:tree[k]=value
            k+=k&-k
    out=[];k=0
    while k<len(order):
        i=order[k];j=k+1
        while j<len(order) and A[order[j]]==A[i] and B[order[j]]==B[i] and C[order[j]]==C[i]:
            j+=1
        r=ranks[B[i]]
        if query(r)>C[i]:
            out.extend(order[k:j])
        update(r,C[i]);k=j
    return sorted(out)

fronts={}
for subgroup,ids in grps.items():
    for direction in ("Tmax","Tmin"):
        T=[-v for v in tc] if direction=="Tmax" else tc
        for mm,M in (("mean",mean),("weighted",weighted)):
            for objectives in ("temp_elements","temp_mass","elements_mass","all_three"):
                label="S"+subgroup+"|D"+direction+"|M"+mm+"|J"+objectives
                if objectives=="temp_elements":out=sky2(ids,T,count)
                elif objectives=="temp_mass":out=sky2(ids,T,M)
                elif objectives=="elements_mass":out=sky2(ids,count,M)
                else:out=sky3(ids,T,count,M)
                fronts[label]=out
assert len(fronts)==48
# Mathematical invariance control: objective positive scale and offset.
assert sky3(grps["all"],[-x*2+3 for x in tc],count,[4*x+10 for x in weighted])==fronts["Sall|DTmax|Mweighted|Jall_three"]
# Negative control: permute experimental temperatures, preserve structure and distribution.
original_size=len(fronts["Sall|DTmax|Mweighted|Jall_three"])
rng=random.Random(1729)
null_counts=[]
for iteration in range(64):
    perm=tc[:]
    rng.shuffle(perm)
    null_counts.append(len(sky3(grps["all"],[-v for v in perm],count,weighted)))
# Two-sided descriptive permutation deviation from average; not rigorous population inferential design.
mu=statistics.mean(null_counts)
p_two=(1+sum(abs(v-mu)>=abs(original_size-mu) for v in null_counts))/(len(null_counts)+1)
digest=hashlib.sha256(json.dumps(fronts,sort_keys=True,separators=(",",":")).encode()).hexdigest()
reps=collections.Counter(formula)
real_distribution=collections.Counter(count)
sizes={key:len(v) for key,v in fronts.items()}
inverse=collections.Counter(i for v in fronts.values() for i in v)
result={
"schema":"omega.tristan.r18.real-experimental-multifront",
"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
"source_doi":"10.24432/C53P47","archive_sha256":EXPECTED,
"rows":N,"train_feature_count":81,"sample_type":"historical superconducting materials only",
"formula_unique":len(reps),"formula_repeated_rows":sum(n-1 for n in reps.values() if n>1),
"temperature_min_K":min(tc),"temperature_max_K":max(tc),
"temperature_median_K":statistics.median(tc),
"groups":{k:len(v) for k,v in grps.items()},
"element_count_distribution":dict(sorted(real_distribution.items())),
"fronts":len(fronts),"front_sha256":digest,
"front_sizes":sizes,
"all_three_maxTc_weighted_size":original_size,
"all_three_maxTc_weighted_indexes":fronts["Sall|DTmax|Mweighted|Jall_three"],
"front_memberships_total":sum(map(len,fronts.values())),
"inverse_membership_max":max(inverse.values()),
"null_permutations":64,"null_counts":null_counts,
"null_size_mean":mu,"null_size_min":min(null_counts),"null_size_max":max(null_counts),
"null_exploratory_p_two_sided":p_two,
"affine_positive_invariance":"PASS",
"epistemic":"DESCRIPTIVE_HISTORICAL_DATA_ONLY_NOT_PREDICTIVE_OR_CAUSAL",
"scope_limits":[
"No evidence of topology, mycelial or hypercomplex material physics from these columns",
"No non-superconductors in this data; cannot predict whether a compound is superconducting",
"Elemental complexity and mean atomic mass are NOT manufacturing cost",
"Permutation p-value is exploratory and does not establish a new physical law",
"Measured historical records may contain duplicates, measurement variability and sample bias",
"No production selection or synthesis recommendation inferred"]
}
(ROOT/"R18_FRONTS.json").write_text(json.dumps(fronts,sort_keys=True,separators=(",",":")),encoding="utf-8")
(ROOT/"R18_RESULT.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:result[k] for k in ("rows","formula_unique","formula_repeated_rows","groups","temperature_min_K","temperature_max_K","fronts","front_sha256","all_three_maxTc_weighted_size","null_size_mean","null_size_min","null_size_max","null_exploratory_p_two_sided","affine_positive_invariance")}))

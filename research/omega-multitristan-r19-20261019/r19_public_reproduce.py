"""Omega Multi-Tristan R19 - self-contained finite synthetic reproduction.
Python standard library only. No files, private data, network, services, or publication.
Existing literature: Minimum Test Collection (Moret & Shapiro, SIAM 1985).
"""
import itertools,collections,hashlib,json,math
grid=list(itertools.product(range(-8,9),repeat=2))
feasible=[i for i,(x,y) in enumerate(grid) if x*x+y*y<=80]
targets=((4,-4),(-4,4),(2,2))
couplings=(2,1,1)
signs=(1,-1,1)
offsets=(0,4,-4)
sets={"01":(0,1),"02":(0,2),"12":(1,2),"012":(0,1,2)}
def objectives(p,sc,di,coordinates):
    a,b=coordinates
    if di:a,b=abs(a),abs(b)
    if sc:a,b=2*(a//2),2*(b//2)
    tx,ty=targets[p]
    return ((a-tx)**2+(b-ty)**2+couplings[p]*(a-signs[p]*b)**2,
            a*a+b*b,
            (a+b-offsets[p])**2+(p+1)*(a-b)**2)
def dominates(a,b,js):
    return all(a[k]<=b[k] for k in js) and any(a[k]<b[k] for k in js)
fronts={}
for p in range(3):
  for sc in range(2):
    for di in range(2):
      vals={i:objectives(p,sc,di,grid[i]) for i in feasible}
      for sub,js in sets.items():
        key=f"P{p}/S{sc}/D{di}/J{sub}"
        fronts[key]=[i for i in feasible if not any(dominates(vals[j],vals[i],js) for j in feasible if i!=j)]
assert len(fronts)==48 and len(feasible)==249
blob=json.dumps(fronts,sort_keys=True,separators=(",",":")).encode()
sha=hashlib.sha256(blob).hexdigest()
assert sha=="12bf5ebe0e1be9ea15b3057f9e111db50a94af714668f67d04c027cffeb7cdff",sha
keys=sorted(fronts)
signatures={i:sum(1<<j for j,k in enumerate(keys) if i in fronts[k]) for i in feasible}
distinct=sorted(set(signatures.values()))
assert len(distinct)==37
differences=list({a^b for a,b in itertools.combinations(distinct,2)})
forced=sorted({d.bit_length()-1 for d in differences if d.bit_count()==1})
assert [keys[i] for i in forced]==["P1/S0/D0/J01","P1/S0/D1/J12","P1/S1/D0/J01","P1/S1/D0/J12"]
selected=["P0/S1/D1/J02","P1/S0/D0/J01","P1/S0/D0/J012","P1/S0/D1/J02",
          "P1/S0/D1/J12","P1/S1/D0/J01","P1/S1/D0/J12","P1/S1/D1/J01",
          "P2/S1/D0/J02","P2/S1/D1/J02"]
testmask=sum(1<<keys.index(k) for k in selected)
assert len(set(selected))==10 and all(d & testmask for d in differences)
# Any 9-column solution must contain all four individually forced questions.
# Identical columns on all 37 profiles are interchangeable. Test the remaining 27 choose 5.
cols={}
for j in range(48):
    pattern=tuple(bool(u&(1<<j)) for u in distinct)
    cols.setdefault(pattern,j)
assert len(cols)==31
free=[j for j in cols.values() if j not in forced]
assert len(free)==27
mandatory=sum(1<<j for j in forced)
needs=[d for d in differences if not (d&mandatory)]
enumerations=0
for five in itertools.combinations(free,5):
    mask=mandatory
    for j in five:mask|=1<<j
    enumerations+=1
    if all(d&mask for d in needs):
        raise AssertionError("NINE_QUESTION_COUNTEREXAMPLE")
assert enumerations==math.comb(27,5)==80730
pair_covers=[(a,b) for a,b in itertools.combinations(feasible,2)
    if (signatures[a]|signatures[b]).bit_count()==48]
assert len(pair_covers)==5 and (112,144) in pair_covers
assert max(v.bit_count() for v in signatures.values())==44
result={"schema":"omega.r19.public_reproducer","status":"EXACT_FINITE_SYNTHETIC_PASS",
"front_sha256":sha,"feasible_candidates":249,"fronts":48,
"membership_total":sum(map(len,fronts.values())),"observable_classes":37,
"minimum_witness_questions":10,"exhaustively_excluded_nine_sets":80730,
"minimum_front_cover_candidates":2,"covering_pairs":pair_covers,
"no_physical_validation":True}
print(json.dumps(result,sort_keys=True))
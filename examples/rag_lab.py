"""Offline retrieval teaching lab: synthetic data, no credentials or external models.

Hash vectors are lexical features, not neural semantic embeddings. Output is an
extractive evidence bundle, not generated language or an entailment guarantee.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from datetime import date
import hashlib
import json
import math
import re

@dataclass(frozen=True)
class Chunk:
    id: str
    tenant: str
    groups: tuple[str, ...]
    valid_from: str
    valid_to: str | None
    text: str
    source: str

CORPUS = [
    Chunk('hr42:v3:carry','t1',('employees-pk',),'2027-01-01',None,
          'Eligible Pakistan permanent employees may carry forward up to five unused annual leave days. Contractors are excluded.', 'HR-42 v3 / section 7 / page 8'),
    Chunk('hr42:v3:expiry','t1',('employees-pk',),'2027-01-01',None,
          'Carried forward annual leave days expire on 31 March of the following year.', 'HR-42 v3 / section 7 / page 8'),
    Chunk('hr42:v2:carry','t1',('employees-pk',),'2025-01-01','2027-01-01',
          'Eligible Pakistan permanent employees may carry forward up to three unused annual leave days.', 'HR-42 v2 / section 7 / page 7'),
    Chunk('finance:retention','t1',('finance',),'2027-01-01',None,
          'The finance retention schedule is restricted to finance staff.', 'Finance / page 2'),
    Chunk('other:carry','t2',('employees-pk',),'2027-01-01',None,
          'Pakistan employees carry forward ninety unused leave days. PRIVATE OTHER TENANT.', 'Other tenant policy'),
    Chunk('hr42:v3:benefits','t1',('employees-pk',),'2027-01-01',None,
          'Annual benefits enrollment opens each January. Contact HR for enrollment guidance.', 'HR-42 v3 / section 2 / page 3'),
]

def tokens(text: str) -> list[str]:
    return re.findall(r'[a-z0-9]+(?:-[a-z0-9]+)*',text.lower())

def eligible(c: Chunk,tenant: str,groups: set[str],valid_at: str) -> bool:
    point=date.fromisoformat(valid_at)
    return (c.tenant==tenant and bool(groups.intersection(c.groups))
            and date.fromisoformat(c.valid_from)<=point
            and (c.valid_to is None or point<date.fromisoformat(c.valid_to)))

def bm25(query: str, corpus: list[Chunk], k1: float=1.2,b: float=.75):
    if not corpus:return []
    docs=[Counter(tokens(c.text)) for c in corpus]
    avg=sum(sum(d.values()) for d in docs)/len(docs)
    if not avg:return []
    df=Counter(t for d in docs for t in d)
    result=[]
    for c,d in zip(corpus,docs):
        score=0.
        for term in set(tokens(query)):
            tf=d[term]
            if not tf:continue
            idf=math.log(1+(len(corpus)-df[term]+.5)/(df[term]+.5))
            score+=idf*tf*(k1+1)/(tf+k1*(1-b+b*sum(d.values())/avg))
        if score>0:result.append((c.id,score))
    return sorted(result,key=lambda x:(-x[1],x[0]))

def hash_vector(text: str,dimensions: int=128) -> dict[int,float]:
    counts=Counter()
    for term in tokens(text):
        n=int.from_bytes(hashlib.sha256(term.encode()).digest()[:8],'big')
        counts[n%dimensions]+=1
    norm=math.sqrt(sum(v*v for v in counts.values()))
    return {k:v/norm for k,v in counts.items()} if norm else {}

def vector_search(query: str,corpus: list[Chunk]):
    q=hash_vector(query);result=[]
    for c in corpus:
        d=hash_vector(c.text);score=sum(v*d.get(i,0) for i,v in q.items())
        if score>0:result.append((c.id,score))
    return sorted(result,key=lambda x:(-x[1],x[0]))

def rrf(*rankings,c: int=60):
    if c<0:raise ValueError('RRF constant must be nonnegative')
    scores=defaultdict(float)
    for ranking in rankings:
        seen=set()
        for rank,(identifier,_) in enumerate(ranking,1):
            if identifier not in seen:
                scores[identifier]+=1/(c+rank);seen.add(identifier)
    return sorted(scores.items(),key=lambda x:(-x[1],x[0]))

def retrieve(question: str,*,tenant='t1',groups=('employees-pk',),valid_at='2027-01-01',limit=3):
    if limit<1:raise ValueError('limit must be positive')
    # Filter before scoring/fetching. A real store must enforce equivalent scope.
    scope=[c for c in CORPUS if eligible(c,tenant,set(groups),valid_at)]
    lexical=bm25(question,scope);vector=vector_search(question,scope)
    fused=rrf(lexical,vector);by_id={c.id:c for c in scope}
    evidence=[asdict(by_id[key]) for key,_ in fused[:limit]]
    return {'question':question,'scope':{'tenant':tenant,'groups':groups,'date':valid_at},
            'lexical':lexical,'hashed_lexical_vector':vector,'fused':fused,
            'evidence':evidence,'abstained':not evidence,
            'note':'Authorized excerpts only; no LLM generation or semantic sufficiency guarantee.'}

def metrics(ranked_ids: list[str],relevant: set[str],k: int):
    if k<1:raise ValueError('k must be positive')
    top=ranked_ids[:k];hits=set(top)&relevant
    first=next((i for i,key in enumerate(top,1) if key in relevant),None)
    return {'precision_at_k':len(hits)/k,
            'recall_at_k':len(hits)/len(relevant) if relevant else None,
            'reciprocal_rank':1/first if first else 0.}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--question',default='unused leave carry forward')
    parser.add_argument('--group',default='employees-pk')
    parser.add_argument('--tenant',default='t1')
    parser.add_argument('--date',default='2027-01-01')
    args=parser.parse_args()
    result=retrieve(args.question,tenant=args.tenant,groups=(args.group,),valid_at=args.date)
    # Evaluate only the fixed teaching query, rather than mislabel arbitrary inputs.
    if args.question=='unused leave carry forward' and args.tenant=='t1' and args.group=='employees-pk' and args.date=='2027-01-01':
        result['teaching_query_metrics']=metrics([x[0] for x in result['fused']],{'hr42:v3:carry','hr42:v3:expiry'},3)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()

"""ScamShield: rank indexed Markdown chunks for a query, with source references."""
import json, math, sys
from collections import Counter
from pathlib import Path
from ingest import ROOT, tokenize

def search(query, top_k=3):
    idx=json.loads((ROOT/'index.json').read_text(encoding='utf-8'))
    q=Counter(tokenize(query)); idf=idx['idf']
    def weights(tf): return {t:(1+math.log(c))*idf.get(t,0) for t,c in tf.items() if c>0 and t in idf}
    qw=weights(q); qnorm=math.sqrt(sum(v*v for v in qw.values()))
    scored=[]
    for item in idx['chunks']:
        dw=weights(item['tf']); dnorm=math.sqrt(sum(v*v for v in dw.values()))
        score=sum(v*dw.get(t,0) for t,v in qw.items())/(qnorm*dnorm) if qnorm and dnorm else 0
        if score>0:scored.append((score,item))
    return sorted(scored,key=lambda x:-x[0])[:top_k]

def main():
    query=' '.join(sys.argv[1:]).strip() or '如何辨識釣魚郵件？'
    results=search(query)
    print('QUERY:',query)
    if not results: print('NO MATCH: review query, sources, or ingestion.');return
    for score,r in results:
        print(f'\n[{r["source"]} / {r["id"]}] score={score:.3f}\n{r["text"][:600]}')

if __name__=='__main__':main()

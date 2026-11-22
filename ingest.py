"""ScamShield: ingest local Markdown files into a reproducible JSON search index.
Uses Python standard library only; no model calls or API keys.
"""
import json, math, re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WIKI = ROOT / 'wiki'
OUT = ROOT / 'index.json'

def tokenize(text):
    text = text.lower()
    latin = re.findall(r'[a-z0-9]+', text)
    han = re.findall(r'[\u4e00-\u9fff]+', text)
    return latin + [s[i:i+2] for s in han for i in range(len(s)-1)] + [s for s in han if len(s)==1]

def chunks_of(text, max_chars=500):
    parts = re.split(r'\n\s*\n', text.strip())
    chunks, current = [], ''
    for part in parts:
        part=part.strip()
        if not part: continue
        if current and len(current)+len(part)+2 > max_chars:
            chunks.append(current); current=''
        if len(part)>max_chars:
            if current: chunks.append(current); current=''
            chunks.extend(part[i:i+max_chars] for i in range(0,len(part),max_chars))
        else: current = (current+'\n\n'+part).strip()
    if current: chunks.append(current)
    return chunks

def main():
    docs = sorted(WIKI.glob('*.md'))
    docs = [p for p in docs if p.name.lower()!='readme.md']
    if len(docs)<5: raise SystemExit('ERROR: Need at least five .md source documents in wiki/.')
    records=[]
    for path in docs:
        text=path.read_text(encoding='utf-8')
        if len(text.strip())<100: raise SystemExit(f'ERROR: source too short: {path.name}')
        for i, chunk in enumerate(chunks_of(text),1):
            records.append({'id':f'{path.stem}-{i:03d}', 'source':path.name,'text':chunk,'tf':dict(Counter(tokenize(chunk)))})
    df=Counter(t for r in records for t in r['tf'])
    n=len(records)
    idf={t:math.log((n+1)/(f+1))+1 for t,f in df.items()}
    OUT.write_text(json.dumps({'format':'scamshield-tfidf-v1','source_count':len(docs),'chunk_count':n,'idf':idf,'chunks':records},ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'INGEST OK: {len(docs)} source documents, {n} chunks -> {OUT.name}')
    for d in docs: print(' -',d.name)

if __name__=='__main__':main()

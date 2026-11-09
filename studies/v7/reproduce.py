#!/usr/bin/env python3
"""Reproduce V7 results from bundled evidence; standard library only."""
import collections, hashlib, json, math, pathlib, random, re, statistics

ROOT=pathlib.Path(__file__).resolve().parent
DATA_ROOT='66e5ffd2766b3947f1ea1e19e6bdd2e9b0d74e0d2eabb1ed6cd21f182c899bdf'
LEVELS=(2048,8192,24576,32768,65536,131072,196608,261112)
PAT=re.compile(r'prompt (\d+) tokens = (\d+) reused \+ (\d+) read in (\d+) ms \([0-9.]+ tok/s\), (\d+) generated in (\d+) ms \([0-9.]+ tok/s\)')
def sha(b): return hashlib.sha256(b).hexdigest()
def load(name): return json.loads((ROOT/name).read_text())
def require(ok, msg):
    if not ok: raise ValueError(msg)
def plan():
    result={}
    for s in range(5):
        for level in LEVELS:
            order=list(range(10)); random.Random(2353+s*1000000+level).shuffle(order)
            for p, index in enumerate([0]+order):
                for kind in ('reset','cold','cached'):
                    result[f's{s}-l{level}-p{p:02d}-{kind}']=(s,level,p,kind,f'l{level}-p{index:02d}')
        order=list(range(10)); random.Random(2353+s).shuffle(order)
        for p,index in enumerate([0]+order): result[f's{s}-sustained-p{p:02d}']=(s,None,p,'sustained',f'sustained-p{index:02d}')
    return result

def main():
    manifest=load('manifest.json'); files=manifest['files']; required={'messages.json','cases.json','calls.json','recorded-summary.json','source-hashes.json','reproduce.py','README.md','METHODS.md'}
    require(set(manifest)=={'version','files'} and manifest['version']==1 and set(files)==required,'Invalid manifest paths')
    require((ROOT/'manifest.json').read_text()==json.dumps(manifest,sort_keys=True,separators=(',',':'))+'\n','Manifest encoding changed')
    require(sha(json.dumps({k:v for k,v in files.items() if k!='reproduce.py'},sort_keys=True,separators=(',',':')).encode())==DATA_ROOT,'Manifest changed')
    for name,expected in files.items(): require(sha((ROOT/name).read_bytes())==expected,'File hash mismatch: '+name)
    messages=load('messages.json'); cases=load('cases.json'); calls=load('calls.json'); summary=load('recorded-summary.json'); schedule=plan()
    require(set(cases)=={f'l{l}-p{i:02d}' for l in LEVELS for i in range(10)} | {f'sustained-p{i:02d}' for i in range(10)},'Missing expected cases')
    for key,value in messages.items(): require(sha(json.dumps(value,sort_keys=True,separators=(',',':')).encode())==key,'Message hash mismatch')
    seen=set(); counts=collections.Counter(); exclusions=collections.Counter(); metrics=collections.defaultdict(lambda:collections.defaultdict(list)); strict=fenced=0
    for x in calls:
        ident=x['id']; require(ident in schedule and ident not in seen,'Unknown or duplicate ID: '+ident); seen.add(ident)
        _,level,p,kind,caseid=schedule[ident]; measured=p>0 and kind!='reset'; require(x['measured']==measured and x['status']=='completed','Incorrect role')
        require(x['messages_sha256'] in messages,'Missing messages')
        if kind!='reset': require(x['messages_sha256']==cases[caseid]['messages_sha256'],'Case mismatch')
        match=PAT.fullmatch(x['native']); require(match is not None,'Invalid native line'); prompt,reused,read,prefill,generated,decode=map(int,match.groups()); usage=x['usage']
        require(prompt==reused+read and prefill>0 and decode>0 and usage['prompt_tokens']==prompt and usage['completion_tokens']==generated and usage['total_tokens']==prompt+generated,'Native/API counter mismatch')
        require(usage['prompt_tokens_details']['cached_tokens']==reused,'Cache mismatch')
        require(x['done'] is True and x['finish_reason'] in ('stop','length'),'Incomplete response')
        require(not x['reasoning_content'] and not x['tool_calls'],'Unexpected response channels')
        if kind in ('cold','cached'): require(prompt==level and (reused==0 if kind=='cold' else prompt-64<=reused<=prompt),'Context/cache mismatch')
        if kind=='sustained': require(prompt==50,'Sustained input mismatch')
        require(generated <= (8 if kind=='reset' else 1024),'Output limit mismatch')
        require(x['ttft_ns']>=0 and x['wall_ns']>=x['ttft_ns'] and all(v>=0 for v in x['io_delta'].values()),'Invalid timing or I/O')
        if not measured: exclusions['resets' if kind=='reset' else 'warmups']+=1; continue
        group='sustained' if kind=='sustained' else f'context/{level}/{kind}';counts[group]+=1
        if kind!='sustained':
            expected=cases[caseid]['expected']; require(isinstance(expected,dict) and set(expected)=={'KEY_0','KEY_1','KEY_2'},'Missing expected answer')
            try: strict+=json.loads(x['content'])==expected
            except (ValueError,TypeError): pass
            m=re.fullmatch(r'\s*```(?:json)?\s*\n(.*?)\n```\s*',x['content'],re.S)
            if m:
                try: fenced+=json.loads(m.group(1))==expected
                except ValueError: pass
        if kind!='sustained' or generated>=512:
            values={'prefill_s':prefill/1000,'decode_s':decode/1000,'read_token_tps':read/(prefill/1000),'decode_tps':generated/(decode/1000),'ttft_s':x['ttft_ns']/1e9,'wall_s':x['wall_ns']/1e9,'logical_read_bytes':x['io_delta']['rchar'],'physical_read_bytes':x['io_delta']['read_bytes']}
            for k,v in values.items(): metrics[group][k].append(v)
    require(seen==set(schedule) and len(calls)==1375,'Missing calls'); require(exclusions=={'resets':440,'warmups':85},'Exclusion mismatch'); require(len(counts)==17 and all(n==50 for n in counts.values()) and set(counts)==set(summary),'Group mismatch');require(strict==0 and fenced==800,'Correctness mismatch')
    checked=0
    for group, data in metrics.items():
        require(set(data)==set(summary[group]['metrics']),'Metric set mismatch')
        for key,values in data.items():
            expected=summary[group]['metrics'][key]; actual={'n':len(values),'median':statistics.median(values),'min':min(values),'max':max(values)}
            require(all(math.isclose(actual[k],expected[k],rel_tol=1e-12,abs_tol=1e-12) for k in actual),'Metric mismatch: '+group+'/'+key);checked+=1
    require(checked==136,'Incomplete metric groups')
    print(json.dumps({'status':'PASS','calls':len(calls),'measured':sum(counts.values()),'groups':len(counts),'metric_groups':checked,'strict_correct':strict,'fence_correct':fenced,'excluded':dict(exclusions),'sustained_decode_median':statistics.median(metrics['sustained']['decode_tps'])},sort_keys=True))
if __name__=='__main__': main()

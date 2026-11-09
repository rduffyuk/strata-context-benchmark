"""Offline scoring replay. No network, inference, configuration or service operations."""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent


def parse_object(text):
    def pairs(items):
        value = {}
        for key, item in items:
            if key in value:
                raise ValueError('Duplicate key')
            value[key] = item
        return value
    def constant(_):
        raise ValueError('Nonfinite number')
    try:
        value = json.loads(text.strip(), object_pairs_hook=pairs, parse_constant=constant)
        return value if type(value) is dict else None
    except ValueError:
        return None


def main():
    manifest = json.loads((ROOT/'manifest.json').read_text())
    for name, expected in manifest.items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=expected:
            raise ValueError('Package integrity mismatch: '+name)
    cases = json.loads((ROOT/'cases.json').read_text())
    method = json.loads((ROOT/'method.json').read_text())
    responses = json.loads((ROOT/'observed-responses.json').read_text())
    planned = {x['id']:x for x in method['schedule'] if x['kind']!='reset'}
    if len(responses)!=160 or len({x['id'] for x in responses})!=160 or set(planned)!={x['id'] for x in responses}:
        raise ValueError('Expected every one of the 160 unique measured responses')
    counts = {str(level):{kind:dict(n=0,raw_json=0,field_shape=0,exact_values=0,qualified_exact=0)
                         for kind in ['cold','cached']} for level in method['levels']}
    for response in responses:
        slot=planned[response['id']]
        if any(response[k]!=slot[k] for k in ['kind','level','prompt_index','prompt_id']):
            raise ValueError('Response identity mismatch')
        value=parse_object(response['content'])
        raw=value is not None
        shape=raw and sorted(value)==['KEY_0','KEY_1','KEY_2'] and all(type(v)is str and re.fullmatch('[0-9a-f]{16}',v) for v in value.values())
        exact=value==cases[slot['prompt_id']]['expected']
        group=counts[str(slot['level'])][slot['kind']];group['n']+=1
        for key,passed in dict(raw_json=raw,field_shape=shape,exact_values=exact,
                               qualified_exact=exact and response['finish_reason']=='stop').items():
            group[key]+=int(bool(passed))
    print(json.dumps(counts,indent=2))


if __name__=='__main__':
    main()

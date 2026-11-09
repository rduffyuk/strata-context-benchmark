"""Replay retained response scoring offline. Standard library; no inference/network."""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent


def score(content, expected):
    text = content.strip()
    try:
        value = json.loads(text)
        valid = isinstance(value, dict)
    except ValueError:
        value = None
        valid = False
    exact = valid and value == expected
    fields = valid and set(value) == {'KEY_0', 'KEY_1', 'KEY_2'} and all(
        type(v) is str and re.fullmatch('[0-9a-f]{16}', v) for v in value.values())
    fence = re.fullmatch(r'```(?:json)?[ \t]*\r?\n(.*?)\r?\n```', text, re.S | re.I)
    normalized = False
    if fence:
        try:
            normalized = json.loads(fence[1]) == expected
        except ValueError:
            pass
    return dict(raw_json_object_valid=valid, field_contract_valid=bool(fields),
                exact_expected_keys_and_values=exact, exact_after_fence_removal=normalized)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--responses', type=Path, default=ROOT/'observed-responses.json')
    args = parser.parse_args()
    manifest = json.loads((ROOT/'manifest.json').read_text())
    for name, expected in manifest.items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != expected:
            raise ValueError('Package integrity mismatch: '+name)
    cases = json.loads((ROOT/'cases.json').read_text())
    method = json.loads((ROOT/'method.json').read_text())
    responses = json.loads(args.responses.read_text())
    schedule = {x['id']: x for x in method['schedule']}
    if len(responses) != 30 or len({x['id'] for x in responses}) != 30:
        raise ValueError('Expected 30 unique measured responses; do not drop failures')
    counts = {arm: dict(n=0, raw_json_object_valid=0, field_contract_valid=0,
                       exact_expected_keys_and_values=0, exact_after_fence_removal=0)
              for arm in method['arms']}
    for row in responses:
        planned = schedule[row['id']]
        if row['arm'] != planned['arm'] or row['prompt_index'] != planned['prompt_index']:
            raise ValueError('Response identity mismatch')
        case = cases[f'l2048-p{row["prompt_index"]:02d}']
        outcome = score(row['content'], case['expected'])
        counts[row['arm']]['n'] += 1
        for key, passed in outcome.items():
            counts[row['arm']][key] += int(passed and row['finish_reason'] == 'stop')
    print(json.dumps(counts, indent=2))


if __name__ == '__main__':
    main()

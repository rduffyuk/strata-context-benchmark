"""Verify the reviewed export and replay its three fixed offline studies. No GPU/network."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
STUDIES = ('v7', 'json-wording-2k', 'strong-json-context')

def verify():
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
    if manifest.get('schema') != 'strata-benchmark-export/v1':
        raise ValueError('Unknown export manifest')
    files = manifest['files']
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p != ROOT / 'MANIFEST.json'}
    if actual != set(files):
        raise ValueError('Missing or unexpected package files')
    for name, entry in files.items():
        rel = Path(name)
        if rel.is_absolute() or any(x in ('..', '.') for x in rel.parts) or '\\' in name:
            raise ValueError('Unsafe package path')
        path = ROOT / rel
        if path.is_symlink() or not path.resolve().is_relative_to(ROOT.resolve()):
            raise ValueError('Package path escapes root')
        raw = path.read_bytes()
        if len(raw) != entry['bytes'] or hashlib.sha256(raw).hexdigest() != entry['sha256']:
            raise ValueError('Package integrity mismatch: ' + name)


def main():
    verify()
    reports = {}
    for study in STUDIES:
        result = subprocess.run([sys.executable, str(ROOT / 'studies' / study / 'reproduce.py')],
                                capture_output=True, text=True, timeout=60, check=True)
        reports[study] = json.loads(result.stdout)
    print(json.dumps({'status':'VERIFIED_OFFLINE_REPLAY', 'studies':reports,
                      'network_or_model_calls':0}, indent=2))

if __name__ == '__main__':
    main()

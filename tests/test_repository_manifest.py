import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('reproduce_all', Path(__file__).resolve().parents[1] / 'reproduce_all.py')
replay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(replay)


class RepositoryManifestTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.data = self.root / 'study' / 'results.csv'
        self.data.parent.mkdir()
        self.data.write_bytes(b'input,result\n1,2\n')
        data = self.data.read_bytes()
        (self.root / 'MANIFEST.json').write_text(json.dumps({
            'schema': 'strata-benchmark-export/v1',
            'files': {'study/results.csv': {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}},
        }))
        self.root_patch = patch.object(replay, 'ROOT', self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)

    def test_normal_manifest_passes(self):
        replay.verify()

    def test_git_and_signing_sidecars_are_allowed(self):
        (self.root / '.git' / 'objects').mkdir(parents=True)
        (self.root / '.git' / 'objects' / 'object').write_bytes(b'git')
        sidecars = self.root / '.rootweaver' / 'provenance'
        sidecars.mkdir(parents=True)
        (sidecars / 'record.json').write_text('{}')
        (sidecars / 'record.json.sig').write_text('signature')
        replay.verify()

    def test_unexpected_files_are_rejected(self):
        for name in ('extra.txt', '.rootweaver/evil.py', '.rootweaver/provenance/evil.py'):
            with self.subTest(name=name):
                extra = self.root / name
                extra.parent.mkdir(parents=True, exist_ok=True)
                extra.write_text('unexpected')
                with self.assertRaises(ValueError):
                    replay.verify()
                extra.unlink()

    def test_tampered_tracked_file_is_rejected(self):
        self.data.write_bytes(b'input,result\n1,3\n')
        with self.assertRaises(ValueError):
            replay.verify()

    def test_tracked_symlink_is_rejected(self):
        with tempfile.NamedTemporaryFile() as target:
            target.write(self.data.read_bytes())
            target.flush()
            self.data.unlink()
            self.data.symlink_to(target.name)
            with self.assertRaises(ValueError):
                replay.verify()

    def test_signing_sidecar_symlink_is_rejected(self):
        sidecars = self.root / '.rootweaver' / 'provenance'
        sidecars.mkdir(parents=True)
        (sidecars / 'record.json').symlink_to(self.data)
        with self.assertRaises(ValueError):
            replay.verify()


if __name__ == '__main__':
    unittest.main()

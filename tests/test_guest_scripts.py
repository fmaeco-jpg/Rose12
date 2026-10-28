import hashlib
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class GuestScriptTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        self.log = self.root / 'calls'
        self.package = self.root / 'orca.deb'
        self.package.write_bytes(b'test package')
        self.digest = hashlib.sha256(self.package.read_bytes()).hexdigest()
        self.env = os.environ.copy()
        self.env.update(PATH=f'{self.bin}:/usr/bin:/bin', TEST_LOG=str(self.log))
        self.stub('id', 'echo 0')
        self.stub('dpkg', 'echo arm64')
        self.stub('dpkg-deb', 'case "$3" in Package) echo orca-ide;; Architecture) echo arm64;; esac')
        self.stub('apt-get', 'printf "%s\\n" "$*" >> "$TEST_LOG"')

    def stub(self, name, body):
        file = self.bin / name
        file.write_text('#!/bin/sh\n' + body + '\n')
        file.chmod(0o755)

    def run_install(self, *args):
        return subprocess.run([str(ROOT / 'guest/install-orca.sh'), *args], env=self.env, capture_output=True, text=True)

    def test_valid_package_installs_with_dependency_resolution(self):
        result = self.run_install('--confirm-guest', str(self.package), self.digest)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.log.read_text().splitlines(), ['update', f'install -y {self.package}'])

    def test_wrong_hash_never_calls_apt(self):
        result = self.run_install('--confirm-guest', str(self.package), '0' * 64)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('SHA-256 mismatch', result.stderr)
        self.assertFalse(self.log.exists())

    def test_wrong_architecture_never_calls_apt(self):
        self.stub('dpkg', 'echo amd64')
        self.assertNotEqual(self.run_install('--confirm-guest', str(self.package), self.digest).returncode, 0)
        self.assertFalse(self.log.exists())

    def test_unexpected_package_never_calls_apt(self):
        self.stub('dpkg-deb', 'echo other')
        self.assertNotEqual(self.run_install('--confirm-guest', str(self.package), self.digest).returncode, 0)
        self.assertFalse(self.log.exists())

    def test_explicit_confirmation_required(self):
        self.assertNotEqual(self.run_install(str(self.package), self.digest).returncode, 0)
        self.assertFalse(self.log.exists())

    def test_launcher_passes_args_without_disabling_sandbox(self):
        self.stub('id', 'echo 1000')
        self.stub('orca-ide', 'printf "%s\\n" "$@" > "$TEST_LOG"')
        env = dict(self.env, DISPLAY=':0')
        result = subprocess.run([str(ROOT / 'guest/start-orca.sh'), '--example'], env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.log.read_text().splitlines(), ['--example'])

    def test_launcher_requires_display(self):
        self.stub('id', 'echo 1000')
        env = dict(self.env)
        env.pop('DISPLAY', None)
        result = subprocess.run([str(ROOT / 'guest/start-orca.sh')], env=env, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('DISPLAY', result.stderr)


if __name__ == '__main__':
    unittest.main()

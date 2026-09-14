"""Pruebas de seguridad del paquete para sincronizar; no acceden a GitHub."""
import hashlib
import importlib.util
import json
import tempfile
import unittest
import warnings
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('sync_apa7', ROOT / 'proyecto/sincronizar_github.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class SyncPackageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='apa7-sync-test-')
        self.root = Path(self.tmp.name)
        self.files = {'package.json': b'{"version":"5.1.2"}', 'index.html': b'<!doctype html>Fixture', 'Plantilla_Maestra_APA7.html': b'<!doctype html>Fixture'}
        self.files.update({f'plantillas/Modelo_{i}.docx': b'fixture' for i in range(14)})
        self.archive = self.root / 'Word_APA_GitHub_5_1_2.zip'
        self.build()

    def tearDown(self):
        self.tmp.cleanup()

    def build(self, wrong_hash=False):
        manifest = {'edition': '5.1.2', 'files': {k: hashlib.sha256(v).hexdigest() for k, v in self.files.items()}}
        if wrong_hash:
            manifest['files']['index.html'] = '0' * 64
        data = dict(self.files)
        data[sync.MANIFEST] = json.dumps(manifest).encode()
        with ZipFile(self.archive, 'w', ZIP_DEFLATED) as z:
            for name, body in data.items():
                f = self.root / name
                f.parent.mkdir(parents=True, exist_ok=True)
                f.write_bytes(body)
                z.writestr(name, body)

    def test_01_rutas_publicas(self):
        self.assertEqual(sync.safe_path('.github/workflows/pages.yml'), '.github/workflows/pages.yml')

    def test_02_rutas_privadas_y_traversal(self):
        for name in ['../fuera', '/tmp/fuera', '.git/config', '.env', '.env.local', 'documento.apa.json', 'hosts.yml', 'node_modules/a.js', 'uploads/a.txt', 'proyecto/../otro', 'a\\b', 'a//b', 'key.pem']:
            with self.subTest(name=name), self.assertRaises(ValueError):
                sync.safe_path(name)

    def test_03_paquete_coherente(self):
        archive, payload = sync.read_package(self.root)
        self.assertEqual(archive, self.archive)
        self.assertEqual(payload['index.html'], self.files['index.html'])

    def test_04_rechaza_zip_desactualizado(self):
        (self.root / 'index.html').write_text('Cambio no empaquetado')
        with self.assertRaisesRegex(ValueError, 'desactualizado'):
            sync.read_package(self.root)

    def test_05_rechaza_hash_falso(self):
        self.build(wrong_hash=True)
        with self.assertRaisesRegex(ValueError, 'Hash incorrecto'):
            sync.read_package(self.root)

    def test_06_rechaza_pat_simulado(self):
        self.files['nota.txt'] = ('ghp_' + 'x' * 32).encode()
        self.build()
        with self.assertRaisesRegex(ValueError, 'Posible secreto'):
            sync.read_package(self.root)

    def test_07_rechaza_enlaces(self):
        (self.root / 'index.html').unlink()
        (self.root / 'index.html').symlink_to(self.root / 'Plantilla_Maestra_APA7.html')
        with self.assertRaisesRegex(ValueError, 'Enlace'):
            sync.read_package(self.root)

    def test_08_rechaza_entradas_duplicadas(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            with ZipFile(self.archive, 'a') as z:
                z.writestr('index.html', self.files['index.html'])
        with self.assertRaisesRegex(ValueError, 'inconsistente'):
            sync.read_package(self.root)


if __name__ == '__main__':
    unittest.main(verbosity=2)

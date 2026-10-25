import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('prepare_api', ROOT / 'scripts/prepare_api.py')
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)


class APIReferenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / 'api', self.root / 'api')
        shutil.copyfile(ROOT / 'translation-sources.json', self.root / 'translation-sources.json')

    def translation(self):
        return json.loads((self.root / 'api/ja/Array.json').read_text())

    def save(self, data):
        (self.root / 'api/ja/Array.json').write_text(json.dumps(data))

    def test_full_pinned_array_coverage_and_unmodified_examples(self):
        _, modules = api.load(self.root)
        _, _, entries, data = modules['Array']
        self.assertEqual(87, len(entries))
        self.assertEqual(86, sum(bool(item['translation']) for item in data['entries'].values()))
        self.assertEqual(9, sum(len(api.examples(item['original'])) for item in data['entries'].values()))
        self.assertEqual('', data['entries']['prn']['original'])
        self.assertEqual('', data['entries']['prn']['translation'])

    def test_different_commit_and_missing_entries_are_rejected(self):
        data = self.translation()
        data['upstream_commit'] = 'a' * 40
        self.save(data)
        with self.assertRaisesRegex(ValueError, 'different snapshot'):
            api.load(self.root)
        data = json.loads((ROOT / 'api/ja/Array.json').read_text())
        del data['entries']['reduce']
        self.save(data)
        with self.assertRaisesRegex(ValueError, 'identifiers do not match'):
            api.load(self.root)

    def test_changed_source_snapshot_and_description_are_rejected(self):
        data = self.translation()
        data['entries']['reduce']['source_html_sha256'] = '0' * 64
        self.save(data)
        with self.assertRaisesRegex(ValueError, 'description checksum'):
            api.load(self.root)
        self.save(json.loads((ROOT / 'api/ja/Array.json').read_text()))
        snapshot = self.root / 'api/upstream/Array.html'
        snapshot.write_text(snapshot.read_text() + '\n')
        with self.assertRaisesRegex(ValueError, 'snapshot checksum'):
            api.load(self.root)

    def test_changed_code_example_is_rejected(self):
        data = self.translation()
        data['entries']['reduce']['translation'] = data['entries']['reduce']['translation'].replace(
            '(defn sum [x]', '(defn broken [x]')
        self.save(data)
        with self.assertRaisesRegex(ValueError, 'code example differs'):
            api.load(self.root)

    def test_staging_keeps_types_usage_and_pinned_source_fallbacks(self):
        output = self.root / 'pages'
        self.assertEqual(2, api.stage(self.root, output, '/test'))
        page = (output / 'api/core/Array.html').read_text()
        self.assertIn('/test/GLOSSARY.html', page)
        self.assertIn('id="aset-uninitialized"', page)
        self.assertNotIn('href="./StaticArray.html"', page)
        self.assertIn('/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/core/StaticArray.carp', page)
        self.assertIn('原文には説明文がありません', page)
        original = api.parse_reference((self.root / 'api/upstream/Array.html').read_text())[1]
        generated = api.parse_reference(page)[1]
        api.check_metadata('Array', original, generated)
        broken = page.replace('(Fn [(Array a)] (Array a))', '(Fn [] ())')
        self.assertNotEqual(page, broken)
        (output / 'api/core/Array.html').write_text(broken)
        with self.assertRaisesRegex(ValueError, 'signature changed'):
            api.check_metadata('Array', original, api.parse_reference(broken)[1])


if __name__ == '__main__':
    unittest.main()

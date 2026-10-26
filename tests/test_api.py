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
    def test_comment_translations_preserve_strings_characters_and_code(self):
        code = '(print "; note") ; note\n(str \\;) ; note\n(print "say \\"hi\\"; note")'
        record = {'original': '```carp\n' + code + '\n```',
                  'code_comment_translations': {'; note': '; 説明'}}
        expected = '(print "; note") ; 説明\n(str \\;) ; 説明\n(print "say \\"hi\\"; note")'
        self.assertEqual([expected], api.translated_examples(record))

    def test_comment_translation_cannot_target_code_or_output(self):
        for source, replacements in (
                ('(print "; note")', {'; note': '; 説明'}),
                ('(+ 1 2)', {'(+ 1 2)': '(+ 2 2)'}),
                ('; note', {'; note': '; 説明\n(+ 2 2)'}),
                ('; note', {'; note': '(+ 2 2)'}),
                ('; => 3', {'; => 3': '; => 4'})):
            with self.subTest(source=source), self.assertRaises(ValueError):
                api.translated_examples({'original': '```\n' + source + '\n```',
                                         'code_comment_translations': replacements})

    def test_real_comment_translation_still_rejects_changed_executable_code(self):
        path = self.root / 'api/ja/Introspect.json'
        data = json.loads(path.read_text())
        data['entries']['with-copy']['translation'] = data['entries']['with-copy']['translation'].replace(
            '(with-copy + 2)', '(with-copy + 1)')
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'code example differs'):
            api.load(self.root)

    def test_rendered_examples_normalize_common_indentation_as_a_block(self):
        page = ('<div class="module-description"></div><section class="binder">'
                '<h3 id="sample">sample</h3><div class="description">defn</div>'
                '<p class="sig">()</p><div class="doc"><pre><code>'
                '    first\n    second\n</code></pre></div></section>')
        self.assertEqual(['first\nsecond'], api.parse_reference(page)[1]['sample']['code_examples'])

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
        manifest_path = self.root / 'api/snapshot.json'
        manifest = json.loads(manifest_path.read_text())
        manifest['english_source_fallbacks']['StaticArray.html'] = 'core/StaticArray.carp'
        manifest_path.write_text(json.dumps(manifest))
        output = self.root / 'pages'
        self.assertEqual(51, api.stage(self.root, output, '/test'))
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

    def test_batch_coverage_and_core_index_source_are_complete(self):
        manifest, modules = api.load(self.root)
        self.assertEqual(
            {'Array', 'Bench', 'Bool', 'Byte', 'Char', 'Control', 'Debug',
             'Derive', 'Double', 'Float', 'Function', 'Geometry', 'IO', 'IO.Raw',
             'Int', 'Introspect', 'Long', 'Map', 'Maybe', 'Opaque', 'Pair',
             'Pattern', 'Pattern.MatchResult', 'Phantom', 'Pointer', 'Quadruple', 'Quasiquote', 'Result',
             'StaticArray', 'Statistics', 'String', 'System', 'Test', 'Triple', 'Unit',
             'Vector2', 'Vector3', 'VectorN',
             'Dynamic', 'Dynamic.Debug', 'Dynamic.List', 'Dynamic.Map', 'Dynamic.Pair',
             'Dynamic.Path', 'Dynamic.Project', 'Dynamic.Random', 'Dynamic.String', 'Dynamic.Symbol',
             'Globals in Macros.carp', 'Globals in ControlMacros.carp'}, set(modules))
        self.assertEqual(1259, sum(len(data[2]) for data in modules.values()))
        self.assertEqual(1002, sum(bool(record['translation']) for data in modules.values()
                                  for record in data[3]['entries'].values()))
        self.assertEqual(148, sum(len(api.examples(record['original'])) for data in modules.values()
                                 for record in [data[3]['module_documentation'],
                                                *data[3]['entries'].values()]))
        record, _ = api.load_index(self.root, manifest)
        self.assertIn('標準ライブラリ', record['translation'])
        record['upstream_commit'] = 'a' * 40
        (self.root / 'api/ja/core_index.json').write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError, 'Core index: translation targets a different snapshot'):
            api.load(self.root)

    def test_module_navigation_and_cross_module_links_are_staged(self):
        output = self.root / 'pages'
        api.stage(self.root, output, '/test')
        index = (output / 'api/core/index.html').read_text()
        self.assertIn('Core — 標準ライブラリ API リファレンス', index)
        for name in ('Array', 'Bench', 'Bool', 'Byte', 'Char', 'Control',
                     'Debug', 'Derive', 'Double', 'Float', 'Function', 'Geometry',
                     'IO', 'IO.Raw', 'Int', 'Introspect', 'Long', 'Map',
                     'Maybe', 'Opaque', 'Pair', 'Pattern', 'Pattern.MatchResult', 'Phantom',
                     'Pointer', 'Quadruple', 'Quasiquote', 'Result', 'StaticArray', 'Statistics',
                     'String', 'System', 'Test', 'Triple', 'Unit', 'Vector2',
                     'Vector3', 'VectorN'):
            self.assertIn(f'href="{name}.html"', index)
            self.assertTrue((output / f'api/core/{name}.html').is_file())
        maybe = (output / 'api/core/Maybe.html').read_text()
        result = (output / 'api/core/Result.html').read_text()
        self.assertIn('(./Result.html)', maybe)
        self.assertIn('(./Maybe.html)', result)
        self.assertNotIn('モジュール概要の原文',
                         (output / 'api/core/Pattern.MatchResult.html').read_text())

    def test_global_pages_use_encoded_links_and_preserve_native_names(self):
        output = self.root / 'pages'
        api.stage(self.root, output, '/test')
        index = (output / 'api/core/index.html').read_text()
        for name in ('Macros', 'ControlMacros'):
            title = f'Globals in {name}.carp'
            self.assertIn(f'href="Globals%20in%20{name}.carp.html"', index)
            page = (output / f'api/core/{title}.html').read_text()
            self.assertIn(f'<h1>{title}</h1>', page)
            self.assertNotIn('モジュール概要の原文', page)
        dynamic = (output / 'api/core/Dynamic.html').read_text()
        self.assertIn('(./Globals%20in%20ControlMacros.carp.html#comp)', dynamic)
        self.assertIn('LanguageGuide-JP.html#動的関数-dynamic-functions', dynamic)
        self.assertNotIn('/blob/master/', dynamic)
        self.assertNotIn('href="https://carp-lang.github.io/carp-docs/Memory.html"', dynamic)

    def test_io_references_reach_the_correct_module_or_pinned_type_source(self):
        output = self.root / 'pages'
        api.stage(self.root, output, '/test')
        io = (output / 'api/core/IO.html').read_text()
        raw = (output / 'api/core/IO.Raw.html').read_text()
        # Both the translated Markdown and expandable original HTML must resolve.
        self.assertIn('(./IO.Raw.html#stdout)', io)
        self.assertIn('href="./IO.Raw.html#stdout"', io)
        self.assertIn('(./IO.html#open-file)', raw)
        self.assertIn('href="./IO.html#open-file"', raw)
        for page in (io, raw):
            self.assertNotIn('href="#file"', page)
            self.assertNotIn('](#file)', page)
            self.assertIn('/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/core/IO.carp#L3', page)
        self.assertIn('href="#SEEK-CUR"', raw)
        self.assertIn('href="#EOF"', raw)

    def test_new_translations_replace_fallbacks_and_show_overview_notes(self):
        output = self.root / 'pages'
        api.stage(self.root, output, '/test')
        array = (output / 'api/core/Array.html').read_text()
        static = (output / 'api/core/StaticArray.html').read_text()
        self.assertIn('[`StaticArray`](./StaticArray.html)', array)
        self.assertNotIn('[`StaticArray`(英語)]', array)
        self.assertIn('変更不可能 (immutable)', static)
        self.assertIn('overview_note_0', static)


if __name__ == '__main__':
    unittest.main()

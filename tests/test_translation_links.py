import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/check_translation_links.py'
spec = importlib.util.spec_from_file_location('translation_links', SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
COMMIT = 'a' * 40
BASE = f'https://github.com/carp-lang/Carp/blob/{COMMIT}/docs/'


class LinkPolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = {
            'snapshot_date': '2026-10-19',
            'upstream_repository': 'carp-lang/Carp',
            'upstream_commit': COMMIT,
            'documents': [{'source': 'docs/Guide.md', 'translation': 'Guide-JP.md',
                           'source_blob': 'b' * 40}],
            'external_english_urls': ['https://example.com/english'],
        }
        self.header = f'# ガイド (Guide)\n\n原文: [Guide.md(英語)]({BASE}Guide.md)\n\n'
        self.write('Guide-JP.md', self.header)

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def check(self):
        self.write('translation-sources.json', json.dumps(self.manifest))
        return checker.check(self.root)

    def test_untranslated_english_fallback_and_original_link_are_valid(self):
        self.write('Guide-JP.md', self.header + f'[Memory.md(英語)]({BASE}Memory.md)\n')
        self.assertEqual([], self.check())

    def test_source_link_must_follow_title(self):
        self.write('Guide-JP.md', '# ガイド\n説明\n' + self.header)
        self.assertTrue(any('title must' in e for e in self.check()))

    def test_english_suffix_must_not_have_a_space(self):
        for label in ['Memory.md', 'Memory.md (英語)', 'Memory.md（英語）']:
            with self.subTest(label=label):
                self.write('Guide-JP.md', self.header + f'[{label}]({BASE}Memory.md)\n')
                self.assertTrue(any('English document label' in e for e in self.check()))

    def test_upstream_moving_ref_is_rejected(self):
        self.write('Guide-JP.md', self.header + '[Memory(英語)](https://github.com/carp-lang/Carp/blob/master/docs/Memory.md)')
        self.assertTrue(any('pinned commit' in e for e in self.check()))

    def test_missing_local_untranslated_document_is_rejected(self):
        self.write('Guide-JP.md', self.header + '[Memory](Memory.md)')
        self.assertTrue(any('local link target is missing' in e for e in self.check()))

    def test_new_translation_requires_existing_references_to_be_updated(self):
        self.manifest['documents'].append({'source': 'docs/Memory.md',
            'translation': 'Memory-JP.md', 'source_blob': 'c' * 40})
        self.write('Memory-JP.md', f'# メモリ\n\n原文: [Memory.md(英語)]({BASE}Memory.md)\n')
        self.write('Guide-JP.md', self.header + f'[Memory(英語)]({BASE}Memory.md)')
        self.assertTrue(any('use Japanese translation' in e for e in self.check()))
        self.write('Guide-JP.md', self.header + '[メモリ](Memory-JP.md)')
        self.assertEqual([], self.check())

    def test_explicit_source_reference_is_allowed(self):
        self.write('Guide-JP.md', self.header + f'原文参照: [Guide(英語)]({BASE}Guide.md)')
        self.assertEqual([], self.check())

    def test_code_examples_are_not_links(self):
        self.write('Guide-JP.md', self.header + '```markdown\n[例](missing.md)\n```\n`[例](missing.md)`\n')
        self.assertEqual([], self.check())

    def test_api_name_inside_link_label_is_preserved(self):
        self.write('Guide-JP.md', self.header + f'[`drop` インターフェース(英語)]({BASE}Drop.md)')
        self.assertEqual([], self.check())
        self.write('Guide-JP.md', self.header + f'[`drop` インターフェース]({BASE}Drop.md)')
        self.assertTrue(any('English document label' in e for e in self.check()))

    def test_japanese_link_must_not_be_marked_english(self):
        self.write('Guide-JP.md', self.header + '[ガイド(英語)](Guide-JP.md)')
        self.assertTrue(any('Japanese translation must not' in e for e in self.check()))

    def test_external_english_and_local_license_labels_are_checked(self):
        self.write('LICENSE', 'License text')
        self.write('Guide-JP.md', self.header + '[参考](https://example.com/english)\n[License](LICENSE)')
        self.assertEqual(2, len(self.check()))

    def test_raw_links_use_same_policy(self):
        self.write('Guide-JP.md', self.header + '[原文](https://raw.githubusercontent.com/carp-lang/Carp/master/docs/Memory.md)')
        self.assertTrue(any('pinned commit' in e for e in self.check()))
        self.assertTrue(any('English document label' in e for e in self.check()))

    def test_duplicate_and_invalid_manifest_entries_are_rejected(self):
        self.manifest['documents'] *= 2
        self.assertTrue(any('duplicate' in e for e in self.check()))
        self.manifest['documents'][0] = {'source': '../secret', 'translation': 'bad.md', 'source_blob': 'short'}
        self.assertTrue(any('invalid source' in e for e in self.check()))


if __name__ == '__main__':
    unittest.main()

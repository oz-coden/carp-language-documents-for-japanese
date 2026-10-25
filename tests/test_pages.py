import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


prepare = load('prepare_pages')
checker = load('check_pages')


class PublicationTests(unittest.TestCase):
    def test_format_string_delimiters_are_literal_in_jekyll(self):
        self.assertEqual("(fstr \"{{ '{{' }}{}\" 1) {{ '{%' }} tag %}",
                         prepare.escape_liquid('(fstr "{{{}" 1) {% tag %}'))

    def test_nested_links_keep_queries_fragments_and_api_labels(self):
        original = '[`API`](../Guide.md?view=1#日本語) [外部](https://example.com/a.md#x)'
        actual = prepare.rewrite_links(original, 'docs/core/README-JP.md', {'docs/Guide.md'})
        self.assertEqual('[`API`]({{ site.baseurl }}/docs/Guide.html?view=1#日本語) '
                         '[外部](https://example.com/a.md#x)', actual)

    def test_markdown_examples_are_not_rewritten(self):
        original = ('`[example](missing.md)`\n```markdown\n[example](missing.md)\n```\n'
                    '~~~markdown\n[example](missing.md)\n~~~\n')
        self.assertEqual(original, prepare.rewrite_links(original, 'README.md', set()))

    def test_unpublished_local_document_fails(self):
        with self.assertRaisesRegex(ValueError, 'unsupported local link'):
            prepare.rewrite_links('[missing](missing.md)', 'README.md', set())

    def test_staging_preserves_all_source_files_and_indexes_same_document(self):
        with tempfile.TemporaryDirectory() as temp:
            sources = list(ROOT.glob('*.md')) + list((ROOT / 'docs').rglob('*.md'))
            before = {path: path.read_bytes() for path in sources}
            destination = Path(temp) / 'pages'
            self.assertEqual(31, prepare.stage(ROOT, destination, '/test', 'https://example.com'))
            self.assertEqual(before, {path: path.read_bytes() for path in sources})
            self.assertEqual((destination / 'index.md').read_text(),
                             (destination / 'docs/index-JP.md').read_text())
            self.assertIn('/docs/Manual-JP.html', (destination / 'index.md').read_text())
            self.assertIn("{{ '{{' }}", (destination / 'docs/Format_Strings-JP.md').read_text())
            self.assertFalse((destination / 'scripts').exists())
            self.assertFalse((destination / '.github').exists())

    def test_generated_link_checker_handles_base_path_and_unicode_anchors(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp)
            (destination / 'assets/css').mkdir(parents=True)
            (destination / 'assets/css/style.css').write_text('')
            page = destination / 'index.html'
            page.write_text('<html lang="ja"><h1 id="日本語">見出し</h1>'
                            '<a href="/test/#%E6%97%A5%E6%9C%AC%E8%AA%9E">見出し</a></html>')
            self.assertEqual([], checker.check(destination, '/test', {'index.html'}))
            page.write_text('<html lang="ja"><a href="/test/#missing">欠落</a>'
                            '<a href="/outside.html">範囲外</a></html>')
            errors = checker.check(destination, '/test', {'index.html', 'missing.html'})
            self.assertTrue(any('missing anchor' in error for error in errors))
            self.assertTrue(any('escapes the Pages base path' in error for error in errors))
            self.assertTrue(any('missing published page' in error for error in errors))


if __name__ == '__main__':
    unittest.main()

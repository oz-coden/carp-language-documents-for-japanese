"""Stage existing Markdown for Jekyll without editing translation sources."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import posixpath
import re
import shutil
from urllib.parse import unquote, urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r'(?<!!)\[([^\]\n]+)\]\(([^\s)]+)\)')
INLINE_CODE = re.compile(r'(`+)(.*?)\1')


def rewrite_links(text: str, source: str, pages: set[str]) -> str:
    """Rewrite local document links, retaining examples, URLs and fragments."""
    result = []
    fence = None
    for line in text.splitlines(keepends=True):
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            result.append(line)
            continue
        if fence is not None:
            result.append(line)
            continue
        code = list(INLINE_CODE.finditer(line))

        def replace(match):
            if any(span.start() <= match.start() and match.end() <= span.end()
                   for span in code):
                return match.group(0)
            label, url = match.groups()
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc or not parsed.path:
                return match.group(0)
            target = posixpath.normpath(posixpath.join(
                posixpath.dirname(source), unquote(parsed.path)))
            if target in pages:
                target = str(Path(target).with_suffix('.html'))
            elif target not in {'LICENSE', 'translation-sources.json'}:
                raise ValueError(f'{source}: unsupported local link: {url}')
            rewritten = urlunsplit(('', '', '/' + target, parsed.query, parsed.fragment))
            return f'[{label}]({{{{ site.baseurl }}}}{rewritten})'

        result.append(LINK.sub(replace, line))
    return ''.join(result)


def stage(root: Path, destination: Path, baseurl: str, url: str) -> int:
    if destination.exists():
        raise ValueError(f'destination already exists: {destination}')
    manifest = json.loads((root / 'translation-sources.json').read_text())
    pages = {entry['translation'] for entry in manifest['documents']}
    pages.update({'README.md', 'GLOSSARY.md', 'TRANSLATION.md', 'CONTRIBUTING.md'})
    shutil.copytree(root / '.pages', destination)
    config = {'baseurl': baseurl.rstrip('/'), 'url': url.rstrip('/'),
              'upstream_commit': manifest['upstream_commit'],
              'source_repository': 'https://github.com/oz-coden/carp-language-documents-for-japanese'}
    with (destination / '_config.yml').open('a') as stream:
        for key, value in config.items():
            stream.write(f'{key}: {json.dumps(value, ensure_ascii=False)}\n')
    for source in sorted(pages):
        original = (root / source).read_text()
        title = original.splitlines()[0].lstrip('# ').strip().replace('`', '')
        front = ('---\n' + f'title: {json.dumps(title, ensure_ascii=False)}\n'
                 + f'source_path: {json.dumps(source)}\n' + '---\n')
        content = front + rewrite_links(original, source, pages)
        output = destination / source
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content)
        if source == 'docs/index-JP.md':
            (destination / 'index.md').write_text(content)
    for asset in ('LICENSE', 'translation-sources.json'):
        shutil.copyfile(root / asset, destination / asset)
    return len(pages) + 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, default=ROOT / '.pages-source')
    parser.add_argument('--baseurl', default='/carp-language-documents-for-japanese')
    parser.add_argument('--url', default='https://oz-coden.github.io')
    args = parser.parse_args()
    count = stage(ROOT, args.destination, args.baseurl, args.url)
    print(f'Prepared {count} pages in {args.destination}')

"""Validate generated HTML, local links, fragments and publication coverage."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.lang = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'html':
            self.lang = attrs.get('lang')
        for attribute in ('href', 'src'):
            if attrs.get(attribute):
                self.links.append(attrs[attribute])


def check(destination: Path, baseurl: str, expected: set[str]) -> list[str]:
    destination = destination.resolve()
    prefix = baseurl.rstrip('/')
    errors = []
    pages = {path.resolve(): Page(path.read_text())
             for path in destination.rglob('*.html')}
    for name in sorted(expected):
        if (destination / name).resolve() not in pages:
            errors.append(f'missing published page: {name}')
    if not (destination / 'assets/css/style.css').is_file():
        errors.append('missing Primer stylesheet')
    for source, page in pages.items():
        name = source.relative_to(destination)
        if page.lang != 'ja':
            errors.append(f'{name}: missing Japanese document language')
        for link in page.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            path = unquote(parsed.path)
            if path.startswith('/'):
                if prefix and not path.startswith(prefix + '/'):
                    errors.append(f'{name}: link escapes the Pages base path: {link}')
                    continue
                target = destination / path[len(prefix):].lstrip('/')
            elif path:
                target = source.parent / path
            else:
                target = source
            target = target.resolve()
            if not target.is_relative_to(destination):
                errors.append(f'{name}: link escapes generated site: {link}')
                continue
            if target.is_dir():
                target = target / 'index.html'
            if not target.is_file():
                errors.append(f'{name}: missing link target: {link}')
                continue
            if parsed.fragment and target in pages:
                if unquote(parsed.fragment) not in pages[target].ids:
                    errors.append(f'{name}: missing anchor: {link}')
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--baseurl', default='/carp-language-documents-for-japanese')
    args = parser.parse_args()
    data = json.loads((ROOT / 'translation-sources.json').read_text())
    sources = {entry['translation'] for entry in data['documents']}
    sources.update({'README.md', 'GLOSSARY.md', 'TRANSLATION.md', 'CONTRIBUTING.md', 'index.md', 'api/README.md'})
    expected = {str(Path(source).with_suffix('.html')) for source in sources}
    api = json.loads((ROOT / 'api/snapshot.json').read_text())
    expected.add('api/core/index.html')
    expected.update(f'api/core/{name}.html' for name in api['modules'])
    problems = check(args.destination, args.baseurl, expected)
    if problems:
        raise SystemExit('\n'.join(problems))
    print(f'Published HTML: {len(expected)} pages, local links and anchors OK')

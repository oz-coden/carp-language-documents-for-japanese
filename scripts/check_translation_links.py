"""Check the repository's inline Markdown links without network access."""

from __future__ import annotations

import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import unquote, urlsplit


LINK = re.compile(r'(?<!!)\[([^\]\n]+)\]\(([^\s)]+)\)')
SHA = re.compile(r'[0-9a-f]{40}')
ENGLISH_LABEL = re.compile(r'\S.*\S\(英語\)|[^\s]\(英語\)')


def prose_lines(text: str):
    """Yield line numbers and prose, excluding fences and inline code."""
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None:
            links = list(LINK.finditer(line))

            def remove_inline_code(match):
                # API names inside a link label are prose; an entire example
                # link enclosed in inline code is not a real link.
                if any(link.start() < match.start() and match.end() < link.end()
                       for link in links):
                    return match.group(2)
                return ''

            yield number, re.sub(r'(`+)(.*?)\1', remove_inline_code, line)


def relative_path(value):
    return (isinstance(value, str) and bool(value)
            and not PurePosixPath(value).is_absolute()
            and '..' not in PurePosixPath(value).parts
            and '\\' not in value)


def check(root: Path) -> list[str]:
    root = root.resolve()
    errors = []

    def error(path, line, message):
        errors.append(f'{path}:{line}: {message}')

    try:
        data = json.loads((root / 'translation-sources.json').read_text())
        repository = data['upstream_repository']
        commit = data['upstream_commit']
        documents = data['documents']
        english_urls = set(data['external_english_urls'])
        if (not isinstance(repository, str)
                or re.fullmatch(r'[\w.-]+/[\w.-]+', repository) is None
                or not isinstance(commit, str) or SHA.fullmatch(commit) is None
                or not isinstance(documents, list) or not documents
                or data['snapshot_date'] != '2026-10-19'
                or not all(isinstance(u, str) for u in english_urls)):
            raise ValueError('invalid repository, snapshot, commit, or document list')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return [f'translation-sources.json:1: {exc}']

    translations = {}
    seen_translations = set()
    for doc in documents:
        if (not isinstance(doc, dict)
                or not relative_path(doc.get('source'))
                or not relative_path(doc.get('translation'))
                or not isinstance(doc.get('source_blob'), str)
                or SHA.fullmatch(doc['source_blob']) is None):
            error('translation-sources.json', 1, 'invalid source/translation/blob entry')
            continue
        source, target = doc['source'], doc['translation']
        if source in translations or target in seen_translations:
            error('translation-sources.json', 1, 'duplicate source or translation')
        translations[source] = target
        seen_translations.add(target)
        if not (root / target).is_file():
            error(target, 1, 'registered translation is missing')

    source_headers = {}
    for source, target in translations.items():
        path = root / target
        if not path.is_file():
            continue
        lines = list(prose_lines(path.read_text()))
        nonempty = [(n, s) for n, s in lines if s.strip()]
        expected = f'https://github.com/{repository}/blob/{commit}/{source}'
        if (len(nonempty) < 2 or not nonempty[0][1].startswith('# ')
                or not nonempty[1][1].startswith('原文: ')
                or not any(url == expected and ENGLISH_LABEL.fullmatch(label)
                           for label, url in LINK.findall(nonempty[1][1]))):
            error(target, 1, 'title must be followed by its pinned 原文: link with XXX(英語)')
        else:
            source_headers[target] = nonempty[1][0]

    for path in sorted(root.rglob('*.md')):
        if '.git' in path.relative_to(root).parts:
            continue
        relative = path.relative_to(root).as_posix()
        for line_no, line in prose_lines(path.read_text()):
            if re.search(r'\[[^\]]+\]\[[^\]]*\]|<a\s', line):
                error(relative, line_no, 'use inline Markdown links, not reference/HTML links')
            for label, url in LINK.findall(line):
                parsed = urlsplit(url)
                upstream_source = None
                english = url in english_urls
                if parsed.hostname == 'github.com':
                    prefix = f'/{repository}/'
                    if parsed.path.startswith(prefix):
                        parts = parsed.path[len(prefix):].split('/', 2)
                        if parts[0] in ('blob', 'tree'):
                            english = True
                            if len(parts) < 2 or parts[1] != commit:
                                error(relative, line_no, 'upstream document must use the pinned commit')
                            if parts[0] == 'blob' and len(parts) == 3:
                                upstream_source = unquote(parts[2])
                elif parsed.hostname == 'raw.githubusercontent.com':
                    prefix = f'/{repository}/'
                    if parsed.path.startswith(prefix):
                        english = True
                        parts = parsed.path[len(prefix):].split('/', 1)
                        if parts[0] != commit:
                            error(relative, line_no, 'raw upstream document must use the pinned commit')
                        if len(parts) == 2:
                            upstream_source = unquote(parts[1])
                elif not parsed.scheme and not parsed.netloc and parsed.path:
                    target = ((root if parsed.path.startswith('/') else path.parent)
                              / unquote(parsed.path.lstrip('/'))).resolve()
                    if not target.is_relative_to(root) or not target.exists():
                        error(relative, line_no, f'local link target is missing: {parsed.path}')
                    else:
                        target_relative = target.relative_to(root).as_posix()
                        english = target_relative == 'LICENSE'
                        if target_relative in seen_translations and label.endswith('(英語)'):
                            error(relative, line_no, 'Japanese translation must not be labelled 英語')
                if english and ENGLISH_LABEL.fullmatch(label) is None:
                    error(relative, line_no, 'English document label must be XXX(英語), without a space before (英語)')
                if (relative in seen_translations and upstream_source in translations
                        and source_headers.get(relative) != line_no
                        and not line.startswith('原文参照:')):
                    error(relative, line_no, f'use Japanese translation: {translations[upstream_source]}')
    return errors


if __name__ == '__main__':
    problems = check(Path(__file__).resolve().parents[1])
    if problems:
        print('\n'.join(problems), file=sys.stderr)
        sys.exit(1)
    print('Translation links: OK')

"""Publish translated API descriptions alongside the pinned compiler output."""

from __future__ import annotations

import argparse
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import textwrap
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
        'meta', 'param', 'source', 'track', 'wbr'}


class Element:
    def __init__(self, tag, attrs, start, inner_start):
        self.tag, self.attrs = tag, dict(attrs)
        self.start, self.inner_start = start, inner_start
        self.inner_end = self.end = inner_start
        self.children = []

    def all(self):
        yield self
        for child in self.children:
            yield from child.all()

    def by_class(self, name):
        return next(node for node in self.all()
                    if name in node.attrs.get('class', '').split())


class Document(HTMLParser):
    """Retain source ranges, including the upstream nested paragraph markup."""
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source = source
        self.offsets = [0]
        for line in source.splitlines(keepends=True):
            self.offsets.append(self.offsets[-1] + len(line))
        self.root = Element('root', {}, 0, 0)
        self.stack = [self.root]
        self.feed(source)

    def position(self):
        line, column = self.getpos()
        return self.offsets[line - 1] + column

    def handle_starttag(self, tag, attrs):
        start = self.position()
        node = Element(tag, attrs, start, start + len(self.get_starttag_text()))
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            node = self.stack.pop()
            node.inner_end = node.end = node.inner_start

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                node = self.stack[index]
                node.inner_end = self.position()
                node.end = self.source.index('>', node.inner_end) + 1
                del self.stack[index:]
                break

    def inner(self, node):
        return self.source[node.inner_start:node.inner_end]


def text(source, strip=True):
    class Text(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.parts = []

        def handle_data(self, data):
            self.parts.append(data)
    parser = Text()
    parser.feed(source)
    value = ''.join(parser.parts)
    return value.strip() if strip else value


def parse_reference(source):
    document = Document(source)
    entries = {}
    for binder in (node for node in document.root.all()
                   if 'binder' in node.attrs.get('class', '').split()):
        heading = next(node for node in binder.all() if node.tag == 'h3')
        name = heading.attrs['id']
        if name in entries:
            raise ValueError(f'duplicate API identifier: {name}')
        usage = next((node for node in binder.all()
                      if 'args' in node.attrs.get('class', '').split()), None)
        entries[name] = {
            'kind': text(document.inner(binder.by_class('description'))),
            'signature': text(document.inner(binder.by_class('sig'))),
            'usage': text(document.inner(usage)) if usage else '',
            'documentation': document.inner(binder.by_class('doc')),
            'code_examples': [textwrap.dedent(text(document.inner(node), strip=False)).strip('\n')
                              for node in binder.by_class('doc').all() if node.tag == 'pre'],
        }
    return document.inner(document.root.by_class('module-description')), entries


def digest(value):
    return hashlib.sha256(value).hexdigest()


def examples(markdown):
    return [textwrap.dedent(match).strip('\n') for match in re.findall(
        r'^\s*`{3,}[^\n]*\n(.*?)^\s*`{3,}\s*$', markdown, re.M | re.S)]


def load(root):
    manifest = json.loads((root / 'api/snapshot.json').read_text())
    translation_manifest = json.loads((root / 'translation-sources.json').read_text())
    commit = manifest['upstream_commit']
    if commit != translation_manifest['upstream_commit']:
        raise ValueError('API and document snapshots must use the same commit')
    modules = {}
    for name, info in manifest['modules'].items():
        snapshot = (root / info['snapshot']).read_bytes()
        if digest(snapshot) != info['snapshot_sha256']:
            raise ValueError(f'{name}: generated snapshot checksum mismatch')
        overview, entries = parse_reference(snapshot.decode())
        translations = json.loads((root / info['translation']).read_text())
        if translations['upstream_commit'] != commit or translations['module'] != name:
            raise ValueError(f'{name}: translation targets a different snapshot')
        if entries.keys() != translations['entries'].keys():
            raise ValueError(f'{name}: translated API identifiers do not match the snapshot')
        pairs = [(overview, translations['module_documentation'])]
        pairs.extend((entry['documentation'], translations['entries'][key])
                     for key, entry in entries.items())
        for original_html, record in pairs:
            if digest(original_html.encode()) != record['source_html_sha256']:
                raise ValueError(f'{name}: original description checksum mismatch')
            if bool(text(original_html)) != bool(record['translation']):
                raise ValueError(f'{name}: missing or invented translated description')
            if record['source'] not in manifest['source_files']:
                raise ValueError(f'{name}: unregistered original source')
            if examples(record['original']) != examples(record['translation']):
                raise ValueError(f'{name}: a translated code example differs from its source')
        modules[name] = (info, overview, entries, translations)
    asset = manifest['stylesheet']
    if digest((root / asset['path']).read_bytes()) != asset['sha256']:
        raise ValueError('upstream API stylesheet checksum mismatch')
    return manifest, modules


def literal(value):
    return re.sub(r'\{\{|\{%', lambda match: "{{ '" + match.group() + "' }}", value)


def markdown(value, number):
    return (f'{{% capture api_text_{number} %}}\n{literal(value)}\n{{% endcapture %}}'
            + f'{{{{ api_text_{number} | markdownify }}}}')


def stage(root, destination, baseurl):
    manifest, modules = load(root)
    commit = manifest['upstream_commit']
    repository = manifest['upstream_repository']
    github = f'https://github.com/{repository}/blob/{commit}/'
    prefix = baseurl.rstrip('/')
    target = destination / 'api/core'
    target.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(root / manifest['stylesheet']['path'], target / 'carp_style.css')
    shutil.copyfile(root / 'api/assets/japanese.css', target / 'japanese.css')

    def rewrite(value):
        for page, source in manifest['english_source_fallbacks'].items():
            value = value.replace(f'./{page}', github + source)
        return value

    navigation = ('<nav aria-label="ドキュメントの案内">'
                  f'<a href="{prefix}/">ヘルプ索引</a> · '
                  '<a href="index.html">API 索引</a> · '
                  f'<a href="{prefix}/GLOSSARY.html">用語集</a></nav>')
    notice = ('<p>この文書は Carp の開発者・貢献者による英語の API 文書を日本語に翻訳・編集した非公式の文書です。'
              f'翻訳元のコミットは <code>{commit}</code> です。</p>'
              '<p>型と使用形式は、この固定版を無変更でビルドして生成しています。'
              f'<a href="{prefix}/TRANSLATION.html">翻訳方針</a>・'
              f'<a href="{prefix}/api/README.html">API 文書の原典と生成方法</a>を参照してください。</p>')
    sidebar = ('<aside class="logo" aria-label="モジュール一覧">'
               f'<img src="{manifest["logo_url"]}" alt="Carp のロゴ">'
               '<p class="title">Core API · 日本語</p><div class="index"><ul>'
               + ''.join(f'<li><a href="{quote(name)}.html">{html.escape(name)}</a></li>'
                         for name in modules) + '</ul></div></aside>')

    def wrap(title, content):
        return ('---\nlayout: null\n---\n<!DOCTYPE html>\n<html lang="ja"><head>'
                '<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
                f'<meta name="carp-upstream-commit" content="{commit}">'
                f'<title>{html.escape(title)} | Carp 日本語 API</title>'
                '<link rel="stylesheet" href="carp_style.css">'
                '<link rel="stylesheet" href="japanese.css"></head><body>'
                f'<div class="content"><header class="api-banner">{navigation}{notice}</header>'
                f'{sidebar}<main class="module">{content}</main></div></body></html>\n')

    index = ('<h1>標準ライブラリ API リファレンス</h1>'
             '<p>モジュールを選択して、各 API の型・使用形式・日本語の説明を参照できます。</p>'
             '<ul>' + ''.join(f'<li><a href="{quote(name)}.html">{html.escape(name)}</a>'
                             f' — {len(data[2])} 項目（説明文のある項目は翻訳済み）</li>'
                             for name, data in modules.items()) + '</ul>'
             '<p>現在の日本語訳は上記のモジュールを対象としています。'
             'ほかのモジュールへの参照は、固定コミットの英語ソースへ案内します。</p>')
    (target / 'index.html').write_text(wrap('API 索引', index))

    for name, (info, overview, entries, translations) in modules.items():
        body = f'<h1>{html.escape(name)}</h1><div class="module-description">'
        body += markdown(rewrite(translations['module_documentation']['translation']), 'overview')
        body += '</div>'
        body += ('<details class="original" lang="en"><summary lang="ja">モジュール概要の原文</summary>'
                 + literal(rewrite(overview)) + '</details>')
        body += ('<nav class="api-members" aria-label="API 一覧">' + ' · '.join(
            f'<a href="#{quote(key, safe="")}">{html.escape(key)}</a>' for key in entries) + '</nav>')
        for number, (key, entry) in enumerate(entries.items()):
            record = translations['entries'][key]
            body += '<section class="binder">'
            for alias, real in info.get('anchor_aliases', {}).items():
                if real == key:
                    body += f'<span id="{html.escape(alias, quote=True)}"></span>'
            body += (f'<h3 id="{html.escape(key, quote=True)}">'
                     f'<a class="anchor" href="#{quote(key, safe="")}">{html.escape(key)}</a></h3>'
                     f'<div class="description">{html.escape(entry["kind"])}</div>'
                     f'<p class="sig">{html.escape(entry["signature"])}</p>')
            if entry['usage']:
                body += f'<pre class="args">{html.escape(entry["usage"])}</pre>'
            body += '<div class="doc">'
            if record['translation']:
                body += markdown(rewrite(record['translation']), number)
            else:
                body += '<p class="undocumented">この項目の原文には説明文がありません。</p>'
            body += '</div>'
            for note_index, note in enumerate(record.get('notes', [])):
                body += '<aside class="translator-note">' + markdown(
                    '**訳注:** ' + note, f'note_{number}_{note_index}') + '</aside>'
            body += (f'<p class="source-link"><a href="{github}{record["source"]}#L{record["line"]}">'
                     '固定版の定義・説明文(英語)</a></p>')
            if text(entry['documentation']):
                body += ('<details class="original" lang="en"><summary lang="ja">説明文の原文</summary>'
                         + literal(rewrite(entry['documentation'])) + '</details>')
            body += '</section>'
        body += (f'<footer><a href="https://github.com/oz-coden/carp-language-documents-for-japanese/blob/main/{info["translation"]}">'
                 '日本語訳のデータ</a> · '
                 '<a href="https://github.com/oz-coden/carp-language-documents-for-japanese/issues">日本語訳の問題を報告</a>'
                 f' · <a href="{prefix}/TRANSLATION.html">翻訳方針</a></footer>')
        (target / f'{name}.html').write_text(wrap(name, body))
    return len(modules) + 1


def check_metadata(name, original, generated):
    if original.keys() != generated.keys():
        raise ValueError(f'{name}: published API identifiers changed')
    for key in original:
        for field in ('kind', 'signature', 'usage'):
            if original[key][field] != generated[key][field]:
                raise ValueError(f'{name}.{key}: published {field} changed')


def check_built(root, destination):
    manifest, modules = load(root)
    for name, (_, _, original, translations) in modules.items():
        page = (destination / f'api/core/{name}.html').read_text()
        _, generated = parse_reference(page)
        check_metadata(name, original, generated)
        for key in original:
            if examples(translations['entries'][key]['original']) != generated[key]['code_examples']:
                raise ValueError(f'{name}.{key}: published code example changed')
        document = Document(page)
        meta = next(n for n in document.root.all()
                    if n.attrs.get('name') == 'carp-upstream-commit')
        if meta.attrs['content'] != manifest['upstream_commit']:
            raise ValueError(f'{name}: published commit does not match the source')
    print(f'Published API metadata: {len(modules)} modules, identifiers/types/usage unchanged')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, default=ROOT / '.pages-source')
    parser.add_argument('--baseurl', default='/carp-language-documents-for-japanese')
    parser.add_argument('--check-built', type=Path)
    args = parser.parse_args()
    if args.check_built:
        check_built(ROOT, args.check_built)
    else:
        count = stage(ROOT, args.destination, args.baseurl)
        print(f'Prepared {count} API pages')

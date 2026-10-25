# API リファレンスの翻訳 (API Reference Translation)

[日本語 API リファレンス](https://github.oz-coden.com/carp-language-documents-for-japanese/api/core/index.html) は、Carp の固定コミット `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` を対象としています。
翻訳対象の版・用語・訳注は、[翻訳方針](../TRANSLATION.md) と [用語集](../GLOSSARY.md) に従います。

Core の索引の案内文と、次の 6 モジュールの概要・説明文を翻訳しています。

| モジュール | 掲載項目 | 説明文の翻訳 |
| --- | --- | --- |
| `Array` | 87 | 86 |
| `Bool` | 11 | 2 |
| `Control` | 6 | 6 |
| `Function` | 2 | 2 |
| `Maybe` | 30 | 28 |
| `Result` | 28 | 28 |
| 合計 | 164 | 152 |

原文に説明文がない 12 項目は、その旨を表示します。型シグネチャ・API 名・使用形式を保持し、説明文に含まれるコード例 13 件も保持しています。

## 原典と生成元 (Sources and Generation)

説明文は、[Array.carp(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/core/Array.carp) などの `doc` メタデータと、[ArrayTemplates.hs(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/src/ArrayTemplates.hs) などに埋め込まれた文字列に由来します。
`ArrayExt.carp`・`Sort.carp`・`String.carp` で追加される項目も含みます。

対象コミットのソースを変更せずにビルドし、本家の [生成スクリプト(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/core/generate_core_docs.carp) で生成した HTML を、API 名・型・使用形式・原文の基準にしています。
本家の Web 公開済み文書は、今回の固定版と同一とは限らないため、型や説明文の基準にはしていません。

| ファイル | 用途 |
| --- | --- |
| `api/snapshot.json` | 対象コミット、原典の blob SHA、生成記録、HTML・CSS の SHA-256、モジュールの対応 |
| `api/upstream/Array.html` | 固定版から生成した、変更していない英語の API 文書 |
| `api/upstream/core_index.html` | 固定版から生成した、変更していない Core の索引 |
| `api/ja/Array.json` | API ごとの原文・日本語訳・原典の位置・訳注・説明文のチェックサム |
| `api/ja/core_index.json` | Core の案内文の原文・日本語訳・原典の位置・チェックサム |
| `api/assets/carp_style.css` | 固定版の API 文書の CSS |
| `api/assets/japanese.css` | 日本語表示と画面幅に合わせた調整 |
| `scripts/prepare_api.py` | 対応関係の検査、Pages 用の生成、公開後の API 情報の検査 |

原典は [RenderDocs.hs(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/src/RenderDocs.hs) によって HTML 化されます。
各モジュールの生成済み HTML と訳文データは、それぞれ `api/upstream/<モジュール名>.html` と `api/ja/<モジュール名>.json` に保存します。
日本語版はこの出力の構成・CSS を使い、原文を開いて確認できる表示を加えています。未翻訳のモジュールへの参照は、固定版の英語ソースへ案内します。

## 訳文の更新と検査 (Updating and Checking Translations)

1. `api/ja/<モジュール名>.json` の対象項目を確認します。`source` と `line` が原典を示します。
2. `translation` を Markdown として修正します。補足は `notes` に記載し、原文と区別します。
3. 原文に含まれるコード例を保持し、原典を変更する場合は固定版と対応関係を再確認します。
4. 次の検査を実行します。

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_translation_links.py
```

`main` の更新時には、通常の文書とともに API 文書も生成・公開します。
公開前に、全対象項目の対応、説明文のチェックサム、コード例、生成後の API 名・型・使用形式、HTML のリンクを検査します。
コード例の実行確認は、これらの検査とは別に行います。

## 固定版の API 文書を再生成する (Regenerating the Pinned API Reference)

GitHub Actions の `Generate pinned API snapshot` を手動実行すると、対象コミットをビルドし、標準ライブラリの英語 API 文書を成果物として保存します。
GHC は `9.6.6`、Stack の resolver は本家の `lts-22.44` を使用します。

生成した HTML を `api/upstream/` に保存し、原典・生成物のハッシュと生成記録を `api/snapshot.json` に記録します。
翻訳データには対応する説明文の SHA-256 を記録し、API 名が生成結果と一致することを確認します。
再生成結果は自動ではリポジトリへ書き戻しません。通常の訳文修正や Pages の公開では、保存済みの固定版 HTML を使用します。

# Carp 日本語ドキュメント (Carp Documentation in Japanese)

[Carp(英語)](https://github.com/carp-lang/Carp) プログラミング言語の公式ドキュメントを日本語に翻訳する、非公式のプロジェクトです。
原著は Carp の開発者・貢献者によるものです。このリポジトリでは、日本語訳の作成、校正、用語と表記の統一を行っています。

## 翻訳対象の版 (Source Snapshot)

**翻訳対象は 2026-10-19 確認時点の英語原文に固定しています。以後の英語原文の変更には追従しません。**
固定版に対する誤訳修正、訳抜けの補完、翻訳品質の改善、新たな文書の翻訳は受け付けます。
これは日本語訳の更新を停止するという意味ではありません。

| 項目 | 内容 |
| --- | --- |
| 原文リポジトリ | [carp-lang/Carp(英語)](https://github.com/carp-lang/Carp) |
| 確認日 | 2026-10-19 (JST) |
| 固定コミット | `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` |
| 原文と訳文の対応 | [translation-sources.json](translation-sources.json) |

日付だけでなくコミットを固定し、原文リンクもこの版を指します。現在の Carp の実装との一致や、コード例がすべて動作することは保証しません。

## 翻訳文書 (Translated Documents)

| 文書 | 原文 | 状態 |
| --- | --- | --- |
| [言語ガイド](LanguageGuide-JP.md) | [LanguageGuide.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/LanguageGuide.md) | 全節を翻訳し、用語・表記を校正しています。原文由来の問題には訳注を付けています |

未翻訳の参考文書へのリンクは省略せず、`文書名(英語)` と明記して英語原文へ案内します。

## 方針と貢献 (Policy and Contributions)

- [翻訳方針](TRANSLATION.md): 翻訳範囲、文体、表記、リンク、訳注の規則です。
- [用語集](GLOSSARY.md): 採用語、英語で保持する語、文脈による例外をまとめています。
- [貢献手順](CONTRIBUTING.md): 修正・新規翻訳の手順と確認方法です。

GitHub Actions で、原文リンク、英語表示、固定版、ローカル文書へのリンク、翻訳済み文書への案内を検査します。
検査は固定情報とリポジトリ内のファイルを使い、原文の更新監視や外部サイトの疎通確認は行いません。

## ライセンスと出典 (License and Attribution)

翻訳元の Carp は [Apache License 2.0(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/LICENSE) で公開されています。
本リポジトリの日本語訳も、そのライセンスを継承し、Apache License 2.0 で公開します。全文は [LICENSE(英語)](LICENSE) を参照してください。

翻訳文書の冒頭に原文へのリンクと、日本語への翻訳・編集を行った旨を記載します。
原著の著作権・帰属表示を保持し、原文と訳者が加えた注釈を区別します。

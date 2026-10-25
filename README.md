# Carp 日本語ドキュメント (Carp Documentation in Japanese)

[Carp(英語)](https://github.com/carp-lang/Carp) プログラミング言語の公式ドキュメントを日本語に翻訳する、非公式のプロジェクトです。
原著は Carp の開発者・貢献者によるものです。このリポジトリでは、日本語訳の作成、校正、用語と表記の統一を行っています。

[Web 版の日本語ドキュメント](https://github.oz-coden.com/carp-language-documents-for-japanese/) では、ヘルプ索引から各文書を参照できます。

日本語訳について気になる点があれば、[問題の報告先](#問題の報告先-reporting-problems) を確認してください。

## Carp について (About Carp)

Carp は、ゲーム、音響合成 (sound synthesis)、可視化など、対話的な操作や性能が重要になる用途に適するよう設計されたプログラミング言語です。

Carp の主な特徴は、次のとおりです。

- 自動的かつ決定論的なメモリ管理 (deterministic memory management) を行います。ガベージコレクタも実行時の VM も使いません。
- 型推論を備えた静的型付けにより、高速性と信頼性を実現します。
- 所有権の追跡 (ownership tracking) により、内部ではキャッシュ効率のよいデータ構造を書き換えつつ、関数型のプログラミングスタイルを利用できます。
- 隠れた性能コストはありません。メモリの割り当てとコピー (copying) は明示的です。
- 既存の C コードと容易に連携できます。
- Lisp マクロ、コンパイル時のスクリプト実行、便利な REPL を備えています。

### さらに詳しく (Learn more)

- [ヘルプ索引](docs/index-JP.md): 目的に合わせて文書を探せます。
- [コンパイラマニュアル](docs/Manual-JP.md): コンパイラのインストール方法と使い方です。
- [Carp 言語ガイド](docs/LanguageGuide-JP.md): 言語の構文と意味論を説明しています。
- [Core のドキュメント(英語)](http://carp-lang.github.io/carp-docs/core/core_index.html): 標準ライブラリのドキュメントです。

### 最小限の例 (A Very Small Example)

```clojure
(load-and-use SDL)

(defn tick [state]
  (+ state 10))

(defn draw [app rend state]
  (bg rend &(rgb (/ @state 2) (/ @state 3) (/ @state 4))))

(defn main []
  (let [app (SDLApp.create "The Minimalistic Color Generator" 400 300)
        state 0]
    (SDLApp.run-with-callbacks &app SDLApp.quit-on-esc tick draw state)))
```

Carp のコードを実行する手順は、[コードの実行方法](docs/HowToRunCode-JP.md) を参照してください。

ほかの例は、[examples ディレクトリ(英語)](https://github.com/carp-lang/Carp/tree/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/examples) を参照してください。

本家 README の全文訳は [Carp の紹介](Carp-JP.md) を参照してください。

## 翻訳対象の版 (Source Snapshot)

**翻訳対象は、Carp のコミット `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` の英語原文に固定しています。以後の英語原文の変更には追従しません。**
この固定版を対象に、誤訳修正、訳抜けの補完、用語・表記の改善、新たな文書の翻訳を行います。

参考資料として [変更履歴の日本語訳](CHANGELOG-JP.md) も掲載しています。原文の収録範囲は 0.5.1〜0.5.5 であり、固定コミットまでのすべての変更を網羅するものではありません。

| 項目 | 内容 |
| --- | --- |
| 原文リポジトリ | [carp-lang/Carp(英語)](https://github.com/carp-lang/Carp) |
| 確認日 | 2026-10-19 (JST) |
| 固定コミット | `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` |
| 原文と訳文の対応 | [translation-sources.json](translation-sources.json) |

文書内の Carp 原文へのリンクは、上記の固定コミットを指します。

## 翻訳文書 (Translated Documents)

固定版の翻訳対象である Markdown 文書 26 ファイルの全文訳を掲載しています。

訳文は原文と同じディレクトリ階層に配置しています。本家 README の全文訳は `Carp-JP.md`、`docs/` の文書は `docs/`、`docs/core/README.md` の訳は `docs/core/README-JP.md` にあります。翻訳方針や用語集、このリポジトリへの貢献手順はトップディレクトリに置いています。

| 文書 | 原文 | 状態 |
| --- | --- | --- |
| [Carp の紹介](Carp-JP.md) | [README.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/README.md) | 全文翻訳済み |
| [変更履歴](CHANGELOG-JP.md) | [CHANGELOG.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/CHANGELOG.md) | 全文翻訳済み (0.5.1〜0.5.5) |
| [言語ガイド](docs/LanguageGuide-JP.md) | [LanguageGuide.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/LanguageGuide.md) | 全文翻訳済み |
| [メモリ管理の詳細](docs/Memory-JP.md) | [Memory.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Memory.md) | 全文翻訳済み |
| [C との相互運用](docs/CInterop-JP.md) | [CInterop.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/CInterop.md) | 全文翻訳済み |
| [インストール](docs/Install-JP.md) | [Install.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Install.md) | 全文翻訳済み |
| [コードの実行方法](docs/HowToRunCode-JP.md) | [HowToRunCode.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/HowToRunCode.md) | 全文翻訳済み |
| [ライブラリ](docs/Libraries-JP.md) | [Libraries.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Libraries.md) | 全文翻訳済み |
| [コンパイラマニュアル](docs/Manual-JP.md) | [Manual.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Manual.md) | 全文翻訳済み |
| [マクロ](docs/Macros-JP.md) | [Macros.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Macros.md) | 全文翻訳済み |
| [準クォート](docs/Quasiquotation-JP.md) | [Quasiquotation.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Quasiquotation.md) | 全文翻訳済み |
| [動的評価器 VM](docs/EvaluatorVM-JP.md) | [EvaluatorVM.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/EvaluatorVM.md) | 全文翻訳済み |
| [動的意味論](docs/DynamicSemantics-JP.md) | [DynamicSemantics.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/DynamicSemantics.md) | 全文翻訳済み |
| [導出](docs/Derive-JP.md) | [Derive.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Derive.md) | 全文翻訳済み |
| [書式指定文字列](docs/Format_Strings-JP.md) | [Format_Strings.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Format_Strings.md) | 全文翻訳済み |
| [`drop` インターフェース](docs/Drop-JP.md) | [Drop.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Drop.md) | 全文翻訳済み |
| [用語 (作成中)](docs/Terminology-JP.md) | [Terminology.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Terminology.md) | 全文翻訳済み |
| [組み込み開発](docs/Embedded-JP.md) | [Embedded.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Embedded.md) | 全文翻訳済み |
| [プログラミングパターン](docs/patterns-JP.md) | [patterns.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/patterns.md) | 全文翻訳済み |
| [マルチメディアライブラリ](docs/Multimedia-JP.md) | [Multimedia.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Multimedia.md) | 全文翻訳済み |
| [開発ツール](docs/Tooling-JP.md) | [Tooling.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Tooling.md) | 全文翻訳済み |
| [本家への貢献ガイド](docs/Contributing-JP.md) | [Contributing.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Contributing.md) | 全文翻訳済み |
| [リリースチェックリスト](docs/ReleaseChecklist-JP.md) | [ReleaseChecklist.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/ReleaseChecklist.md) | 全文翻訳済み |
| [標準ライブラリのドキュメント生成](docs/core/README-JP.md) | [docs/core/README.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/core/README.md) | 全文翻訳済み |
| [ヘルプ索引](docs/index-JP.md) | [index.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/index.md) | 全文翻訳済み |
| [Carp コンパイラの開発](docs/hacking-JP.md) | [hacking.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/hacking.md) | 全文翻訳済み |

未翻訳の参考文書へのリンクは省略せず、`文書名(英語)` と明記して英語原文へ案内します。

## 方針と貢献 (Policy and Contributions)

- [翻訳方針](TRANSLATION.md): 翻訳範囲、文体、表記、リンク、訳注の規則です。
- [用語集](GLOSSARY.md): 採用語、英語で保持する語、文脈による例外をまとめています。
- [貢献手順](CONTRIBUTING.md): 修正・新規翻訳の手順と確認方法です。

## 問題の報告先 (Reporting Problems)

| 問題の対象 | 報告先 |
| --- | --- |
| 日本語訳の誤訳、訳抜け、表現、訳語、訳注、このリポジトリの文書やリンク | [このリポジトリの Issue](https://github.com/oz-coden/carp-language-documents-for-japanese/issues) |
| 英語原文そのもの、Carp 本体の仕様や実装 | [Carp 本家の Issue(英語)](https://github.com/carp-lang/Carp/issues) |

日本語訳に関する問題は、本家の Issue、Gitter、Discord には報告せず、このリポジトリへ報告してください。原文にも同じ問題があるか判断できない場合は、まずこのリポジトリの Issue で相談してください。

報告先は、報告文の言語ではなく、問題の対象によって選んでください。翻訳文書中の本家への連絡・貢献の案内は、英語原文や Carp 本体に関するものです。

## ライセンスと出典 (License and Attribution)

翻訳元の Carp は [Apache License 2.0(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/LICENSE) で公開されています。
本リポジトリの日本語訳も、そのライセンスを継承し、Apache License 2.0 で公開します。全文は [LICENSE(英語)](LICENSE) を参照してください。

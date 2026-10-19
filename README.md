# Carp 日本語ドキュメント (Carp Documentation in Japanese)

[Carp(英語)](https://github.com/carp-lang/Carp) プログラミング言語の公式ドキュメントを日本語に翻訳する、非公式のプロジェクトです。
原著は Carp の開発者・貢献者によるものです。このリポジトリでは、日本語訳の作成、校正、用語と表記の統一を行っています。

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

- [コンパイラマニュアル](Manual-JP.md): コンパイラのインストール方法と使い方です。
- [Carp 言語ガイド](LanguageGuide-JP.md): 言語の構文と意味論を説明しています。
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

Carp のコードを実行する手順は、[コードの実行方法](HowToRunCode-JP.md) を参照してください。

ほかの例は、[examples ディレクトリ(英語)](https://github.com/carp-lang/Carp/tree/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/examples) を参照してください。

本家 README の全文訳は [Carp の紹介](Carp-JP.md) を参照してください。

## 翻訳対象の版 (Source Snapshot)

**翻訳対象は、Carp のコミット `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` の英語原文に固定しています。以後の英語原文の変更には追従しません。**
この固定版を対象に、誤訳修正、訳抜けの補完、用語・表記の改善、新たな文書の翻訳を行います。

| 項目 | 内容 |
| --- | --- |
| 原文リポジトリ | [carp-lang/Carp(英語)](https://github.com/carp-lang/Carp) |
| 確認日 | 2026-10-19 (JST) |
| 固定コミット | `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` |
| 原文と訳文の対応 | [translation-sources.json](translation-sources.json) |

文書内の Carp 原文へのリンクは、上記の固定コミットを指します。

## 翻訳文書 (Translated Documents)

| 文書 | 原文 | 状態 |
| --- | --- | --- |
| [Carp の紹介](Carp-JP.md) | [README.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/README.md) | 全文翻訳済み |
| [言語ガイド](LanguageGuide-JP.md) | [LanguageGuide.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/LanguageGuide.md) | 全文翻訳済み |
| [メモリ管理の詳細](Memory-JP.md) | [Memory.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Memory.md) | 全文翻訳済み |
| [C との相互運用](CInterop-JP.md) | [CInterop.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/CInterop.md) | 全文翻訳済み |
| [インストール](Install-JP.md) | [Install.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Install.md) | 全文翻訳済み |
| [コードの実行方法](HowToRunCode-JP.md) | [HowToRunCode.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/HowToRunCode.md) | 全文翻訳済み |
| [ライブラリ](Libraries-JP.md) | [Libraries.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Libraries.md) | 全文翻訳済み |
| [コンパイラマニュアル](Manual-JP.md) | [Manual.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Manual.md) | 全文翻訳済み |
| [マクロ](Macros-JP.md) | [Macros.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Macros.md) | 全文翻訳済み |
| [準クォート](Quasiquotation-JP.md) | [Quasiquotation.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Quasiquotation.md) | 全文翻訳済み |
| [動的評価器 VM](EvaluatorVM-JP.md) | [EvaluatorVM.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/EvaluatorVM.md) | 全文翻訳済み |
| [動的意味論](DynamicSemantics-JP.md) | [DynamicSemantics.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/DynamicSemantics.md) | 全文翻訳済み |
| [導出](Derive-JP.md) | [Derive.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Derive.md) | 全文翻訳済み |

未翻訳の参考文書へのリンクは省略せず、`文書名(英語)` と明記して英語原文へ案内します。

## 方針と貢献 (Policy and Contributions)

- [翻訳方針](TRANSLATION.md): 翻訳範囲、文体、表記、リンク、訳注の規則です。
- [用語集](GLOSSARY.md): 採用語、英語で保持する語、文脈による例外をまとめています。
- [貢献手順](CONTRIBUTING.md): 修正・新規翻訳の手順と確認方法です。

## ライセンスと出典 (License and Attribution)

翻訳元の Carp は [Apache License 2.0(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/LICENSE) で公開されています。
本リポジトリの日本語訳も、そのライセンスを継承し、Apache License 2.0 で公開します。全文は [LICENSE(英語)](LICENSE) を参照してください。

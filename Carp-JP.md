# Carp

原文: [README.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/README.md)

翻訳元のコミットは `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` です。
この文書は Carp の開発者・貢献者による英語原文を日本語に翻訳・編集した非公式の文書です。
翻訳方針は [TRANSLATION.md](TRANSLATION.md)、採用語は [GLOSSARY.md](GLOSSARY.md) を参照してください。

<img src="https://raw.githubusercontent.com/carp-lang/Carp/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/resources/logo/carp_logo_300_c.png" alt="Carp のロゴ" align="right"/>

公式 Discord サーバーができました ([招待リンク(英語)](https://discord.gg/yyjnBcMqYM))。今後、言語に関する議論は主にこちらで行われることになりそうです。ぜひ参加してください！

[Linux CI(英語)](https://github.com/carp-lang/Carp/actions?query=workflow%3A%22Linux+CI%22) · [MacOS CI(英語)](https://github.com/carp-lang/Carp/actions?query=workflow%3A%22MacOS+CI%22) · [Windows CI(英語)](https://github.com/carp-lang/Carp/actions?query=workflow%3A%22Windows+CI%22)

*警告！ これは研究プロジェクトです。ここにある情報の多くは、説明もなく古くなり、誤解を招くものになる可能性があります。重要な用途には、まだ使わないでください！*

*[言語のバージョン 0.6.0 が公開されました！(英語)](https://github.com/carp-lang/Carp/releases/)*

## Carp について (About)

Carp は、ゲーム、音響合成 (sound synthesis)、可視化など、対話的な操作や性能が重要になる用途に適するよう設計されたプログラミング言語です。

Carp の主な特徴は、次のとおりです。

- 自動的かつ決定論的なメモリ管理 (deterministic memory management) を行います。ガベージコレクタも VM も使いません。
- 型推論を備えた静的型付けにより、高速性と信頼性を実現します。
- 所有権の追跡 (ownership tracking) により、内部ではキャッシュ効率のよいデータ構造を書き換えつつ、関数型のプログラミングスタイルを利用できます。
- 隠れた性能コストはありません。メモリの割り当てとコピー (copying) は明示的です。
- 既存の C コードと容易に連携できます。
- Lisp マクロ、コンパイル時のスクリプト実行、便利な REPL を備えています。

> 訳注: コンパイラ内部では動的評価器 VM が使われています。[評価器 VM の説明](EvaluatorVM-JP.md#現時点で目指していないこと-current-non-goal) では、この VM は利用者のプログラムを実行する VM ではなく、Carp のコンパイル済みコードの実行モデルも変更しないとしています。

## さらに詳しく (Learn more)

- [コンパイラマニュアル](Manual-JP.md): コンパイラのインストール方法と使い方です。
- [Carp 言語ガイド](LanguageGuide-JP.md): 言語の構文と意味論を説明しています。
- [Core のドキュメント(英語)](http://carp-lang.github.io/carp-docs/core/core_index.html): 標準ライブラリのドキュメントです。

[Gitter のチャットに参加する(英語)](https://gitter.im/eriksvedang/Carp?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

## 最小限の例 (A Very Small Example)

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

## メンテナー (Maintainers)

- [Erik Svedäng(英語)](https://github.com/eriksvedang)
- [Veit Heller(英語)](https://github.com/hellerve)
- [Jorge Acereda(英語)](https://github.com/jacereda)
- [Scott Olsen(英語)](https://github.com/scolsen)
- [Tim Dévé(英語)](https://github.com/TimDeve)

## 貢献 (Contributing)

長年にわたり Carp に貢献してくださった [すばらしい皆さん(英語)](https://github.com/carp-lang/Carp/graphs/contributors) に感謝します！

いつでも協力を歓迎しています。まずは [本家への貢献ガイド(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Contributing.md) を参照してください。

## ライセンス (License)

Copyright 2016 - 2021 Erik Svedäng

Apache License, Version 2.0 (以下「本ライセンス」) の下でライセンスされています。
本ライセンスに従う場合を除き、本ファイルを使用することはできません。
本ライセンスの写しは、次の URL から入手できます。

[http://www.apache.org/licenses/LICENSE-2.0(英語)](http://www.apache.org/licenses/LICENSE-2.0)

適用法で義務付けられている場合、または書面で合意した場合を除き、本ライセンスの下で配布されるソフトウェアは「現状のまま」提供され、明示・黙示を問わず、いかなる保証も伴いません。
本ライセンスによる許可と制限を定める具体的な条項については、本ライセンスを参照してください。

`src/carp_regex.h` の正規表現の実装には、MIT ライセンスの条件の下で、次の著作権表示が適用されます。

Copyright (C) 1994-2017 Lua.org, PUC-Rio

詳細は、ライセンスファイル [LUA_LICENSE(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/LUA_LICENSE) を参照してください。

> 訳注: 原文の `src/carp_regex.h` は固定版に存在しません。固定版の [LUA_LICENSE(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/LUA_LICENSE) では、Lua 由来の対象として [core/carp_pattern.h(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/core/carp_pattern.h#L1-L5) が記載されています。

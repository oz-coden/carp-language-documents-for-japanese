# 用語 (作成中) (Terminology (WORK IN PROGRESS))

原文: [Terminology.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Terminology.md)

翻訳元のコミットは `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` です。
この文書は Carp の開発者・貢献者による英語原文を日本語に翻訳・編集した非公式の文書です。
翻訳方針は [TRANSLATION.md](TRANSLATION.md)、採用語は [GLOSSARY.md](GLOSSARY.md) を参照してください。

## はじめに (Introduction)

この文書は、Carp プログラミング言語でよく使われる単語、概念、専門用語をまとめたものです。特に、名前を付けるときや文書を書くときに役立つはずです。曖昧性をなくし、表記をそろえ、Carp のエコシステム全体に統一感を持たせることを目指しています。

この文書への Pull Request は大歓迎です。足りないものがあれば、[Gitter チャンネル(英語)](https://gitter.im/eriksvedang/Carp?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) で教えてください。

> 訳注: この呼びかけは、本家の英語原文への貢献・報告に関するものです。日本語訳や訳語、訳注の問題は、本家ではなく [このリポジトリの Issue](https://github.com/oz-coden/carp-language-documents-for-japanese/issues) へ報告してください。翻訳の問題か原文の問題か判断できない場合も、まずこちらへ相談してください。日本語訳の修正案は、このリポジトリへの Pull Request で受け付けます。

### 値を変更する関数 (Mutating function)

この呼び名は、正確には何を意味する言葉にするべきでしょうか。理想的には、値を変更する関数 (mutating function) という呼び名は、名前が `!` で終わり、`()` を返す関数にだけ使うべきです。「外部を変更する関数 (externally mutating function)」と呼ぶほうがよいでしょうか。それとも「exo-functions」でしょうか :)

### 所有権を取得する関数 (Owning function)

*所有権を取得する関数 (owning function)* は、渡された値の所有権を取得する関数です。つまり、その値のメモリを解放するか、別の所有権を取得する関数に値を渡すか、返り値として返す責任を負います。

### 借用する関数 (Borrowing function)

*借用する関数 (borrowing function)* は、渡された値の所有権を取得しない関数です。つまり、その値のメモリを解放することは許されず、メモリをそのまま保持しなければなりません。

### 値を変換する関数 / endo-functions (Transforming function / endo-functions)

所有権を取得し、内部で値を変更するような、値を変換する関数 (transforming function) には、どのような名前がよいでしょうか。`endo-map` がその例です。このような関数は Carp ではよく使われ、メモリをコピーしたり割り当てたりせずに、関数型のプログラミングスタイルを実現できます。

### 安全でない関数 (Unsafe function)

安全でない関数 (unsafe function) は、ほとんどの場合、名前が接頭辞 `unsafe-` で始まります。特定の前提条件を満たさないと、プログラムをクラッシュさせる *可能性があります*。よい例は、配列の最初の値を取得する `Array.unsafe-first` です。空の配列に対してこれを呼び出すと、プログラムはクラッシュします。

`unsafe-` という接頭辞は、任意の命名規則です。安全でない関数の中には、この命名規則に従わないものも *あります*。代表的な例は `Array.nth` で、不正な添字を渡すとクラッシュします。ほかの安全でない関数も、その性質を文書で十分に説明するべきです。ライブラリのコードでは、`unsafe-` という接頭辞を使うことを強く勧めます。

> 訳注: 対象コミットの `Array.nth` は添字の範囲を検査し、範囲外なら `Maybe.Nothing` を返します。この関数について「不正な添字を渡すとクラッシュする」という原文の説明は、この版の実装と一致しません。[Array.nth の実装(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/core/Array.carp#L408-L414)

### REPL

*REPL* は「Read Eval Print Loop」の略で、Lisp システムによくある機能です。コマンドプロンプトで式を入力し、実行できます。Carp では大文字で表記します。

# 準クォート (Quasiquotation)

原文: [Quasiquotation.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Quasiquotation.md)

翻訳元のコミットは `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` です。
この文書は Carp の開発者・貢献者による英語原文を日本語に翻訳・編集した非公式の文書です。
翻訳方針は [TRANSLATION.md](../TRANSLATION.md)、採用語は [GLOSSARY.md](../GLOSSARY.md) を参照してください。

準クォート (quasiquotation) は、リストの一部をクォートしたまま、ほかの部分を評価する方法です。プログラムの動的な部分でのみ利用できます。

準クォートを使うと、未評価の、つまりクォートされたリストの中に、評価済みの、つまりアンクォート (unquoted) された部分を差し込めます。

```clojure
(defdynamic x 2)

(quasiquote (+ (unquote x) 1)) ; => (+ 2 1)

; リテラルの記法もあり、quasiquote は `、
; unquote は % と書ける
`(+ %x 1) ; => (+ 2 1)
```

アンクォートは `quasiquote` 形式の内部でのみ意味を持ちます。外部で使用すると、マクロ展開時にエラーになります。

準クォートは主にリストを扱うため、別のリストの要素を、入れ子のリストにせずに差し込みたくなることがあります。この操作をスプライシング (splicing) と呼びます。このために、Carp は `unquote-splicing` を提供しています。

```clojure
(defdynamic x '(1 2))

(quasiquote (+ (unquote-splicing x))) ; => (+ 1 2)

; unquote-splicing のリテラルの記法は %@
`(+ %@x) ; => (+ 1 2)
```

ここまでのコード例では変数だけを使っていますが、`unquote` およびその派生形式の内部では、任意の式を使えます。

```clojure
(quasiquote (+ (unquote-splicing (map inc [1 2])))) ; => (+ 2 3)
; または
`(+ %@(map inc [1 2])) ; => (+ 2 3)
```

準クォートは入れ子にできます。`quasiquote` ごとに入れ子の深さが 1 増え、`unquote` または `unquote-splicing` ごとに 1 減ります。深さが 0 になった式だけが評価され、それ以外の形式は結果に保持されるため、入れ子になった準クォートは 1 段階ずつ展開されます。

```clojure
``(x %%(* 2 2)) ; => `(x %4)
``(x %(* 2 2))  ; => `(x %(* 2 2))
```

> 訳注: 固定版の Windows 11 の REPL では、最後の 2 例の結果は、それぞれ `(quasiquote (x (unquote 4)))` と `(quasiquote (x (unquote (* 2 2))))` という名前付き形式で表示されることが確認されています。原文の省略記法による期待値と、構造は同じです。

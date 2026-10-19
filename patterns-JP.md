# Carp のプログラミングパターン (Carp Patterns)

原文: [patterns.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/patterns.md)

翻訳元のコミットは `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` です。
この文書は Carp の開発者・貢献者による英語原文を日本語に翻訳・編集した非公式の文書です。
翻訳方針は [TRANSLATION.md](TRANSLATION.md)、採用語は [GLOSSARY.md](GLOSSARY.md) を参照してください。

この文書では、Carp でよく使われるプログラミングパターン (programming pattern) を紹介します。

## 参照を `let` で束縛する (Ref-let)

外側のスコープにある、参照ではない実引数に対して、所有権を取得する関数 (ownership-taking function) を 2 種類実行し、その結果を計算したい場合があるかもしれません。次の関数を考えてみます。

```clojure
(defn needs-ref-let [x]
  (Pair.init (Maybe.or-zero x) (Maybe.or-zero x)))
```

Carp は、この関数を問題として指摘します。`Maybe.or-zero` が、参照ではなくメモリ管理の対象となる (managed) 実引数 `x` の *所有権を取得する* ためです[^1]。この制約によって、`x` に関連付けられたメモリを何らかの形で書き換えてしまうことを防げるのは、ありがたいことです。もし書き換えてしまえば、結果は予測できなくなります。特に、複数の `Maybe.or-zero` が同時に `x` にアクセスする可能性のある、マルチスレッドの状況では問題になります。

それでも、1 つの `x` の値に対して、両方の `Maybe.or-zero` の呼び出しを計算したい場合もあるでしょう。このような場合は、変数を `x` への `Ref` に束縛 (binding) すると便利です。

```clojure
(defn needs-ref-let [x]
  (let [x* &x]
    (Pair.init (Maybe.or-zero @x*) (Maybe.or-zero @x*))))
```

`x*` は単に引数 `x` への参照であり、これを使えば関数本体のどこでも必要に応じて `x` をコピーできます。もちろん、この例の 2 回目のコピーは、実際には不要です。一度コピーしたあとは、`x` 自体を再び使えるためです。

```clojure
(defn needs-ref-let [x]
  (let [x* &x]
    (Pair.init (Maybe.or-zero @x*) (Maybe.or-zero x))))
```

[^1]: Carp では、`Maybe` のような直和型 (sumtype) は、借用チェッカー (borrow checker) による *メモリ管理の対象* です。つまり、それらに関連付けられたメモリが適切な所有権の下にあり、不要になったときに削除されることを Carp が保証します。すべての型がメモリ管理の対象となるわけではありません。例えば、`Int` はメモリ管理の対象外なので、上で説明した問題は `Int` 型の実引数には当てはまりません。詳しくは [メモリ管理の詳細](Memory-JP.md) を参照してください。

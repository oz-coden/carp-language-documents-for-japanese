# 導出 (Derive)

原文: [Derive.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Derive.md)

翻訳元のコミットは `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` です。
この文書は Carp の開発者・貢献者による英語原文を日本語に翻訳・編集した非公式の文書です。
翻訳方針は [TRANSLATION.md](TRANSLATION.md)、採用語は [GLOSSARY.md](GLOSSARY.md) を参照してください。

`derive` は、データ型のメンバーに基づいて、インターフェースの実装方法を自動的に決める仕組みです。このような実装の導出 (derivation) に使う独自のルールを、導出器 (deriver) として定義することもできます。

自分の型に対して `derive` でインターフェースを実装する方法は、この文書の [第 I 節](#i-derive-の使い方-i-using-derive) を参照してください。インターフェースの導出器を用意する方法は、[第 II 節](#ii-導出器の作成-ii-writing-derivers) を参照してください。

## I: `derive` の使い方 (I: Using `derive`)

ほとんどの場合、`derive` の使い方は単純で、型名と実装するインターフェースを指定して呼び出すだけです。

```clojure
(deftype Point [
  x Int
  y Int
])
(derive Point zero)
(derive Point =)

; 別の関数名で生成したい場合は、第 3 引数に渡す
; 名前の衝突を避けるのに役立つ
(derive Point str my-str)
```

上のコードは、`Point` 型のメンバーに基づいて、その型に対する `zero` と `=` の実装を用意します。この仕組みを使うには、型が *具体的な型 (concrete)*、つまり型変数を含まない型であり、かつ *各メンバーの型がそのインターフェースを実装している* 必要があります。どちらの関数の定義も、メンバーに対する定義に依存するためです。ある型の `zero` は各メンバーの `zero` から作られ、その型の値同士が等しいかどうかは、各メンバーの値同士が等しいかどうかで決まります。

Carp が標準で用意している自動導出 (automatic derivation) の対象は、`=`、`zero`、`str` だけです。ただし、依存するコードが別の導出器を用意している場合もあるので、`(derivables)` を呼び出して確認できます。あるインターフェースが導出可能かを調べるには、`(derivable? <interface>)` を呼び出します。インターフェース名をクォートする必要があることに注意してください。

上記の前提条件のどちらかを満たさない場合、`derive` は使えず、これらの関数を自分で実装する必要があります。

ある型の値を受け取り、すべてのメンバーに同じ処理をして、その値を返すような、更新用のインターフェースを導出したい場合もあります。`Point` でのよい例は `inc` です。

通常は独自の導出器を書く必要があるかもしれませんが、その方法は [第 II 節](#ii-導出器の作成-ii-writing-derivers) で説明します。Carp には、この用途向けに `make-update-deriver` という特別な動的関数があります。値を更新して返す単項インターフェース (unary interface) を受け取り、その値をメンバーとして持つ型全体の定義を組み立てます。`Point` の場合は次のようになります。

```clojure
(make-update-deriver 'inc) ; クォートに注意
(derive Point inc)

(inc (Point.zero)) ; => (Point 1 1)
```

便利な場合もありますが、対象は上記の特定の形の関数に限られます。つまり、`update-<member>` 形式の関数にも渡せる関数にしか使えません。

## II: 導出器の作成 (II: Writing derivers)

標準で用意されていないインターフェースに対して、独自の導出方法を用意したい場合もあります。その場合は、`make-deriver` を使って独自の導出器を用意できます。

動的関数 `make-deriver` は、クォートしたインターフェース名、生成する実装が受け取る引数の名前、型を受け取ってその型に対する実装を生成する関数、という 3 つの引数を取ります。

少し奇妙に聞こえるかもしれないので、`zero` の導出器を例に考えてみましょう。

```clojure
(make-deriver 'zero []
  (fn [t]
    (cons 'init
      (map (fn [_] '(zero)) (members t)))))
```

> 訳注: 対象コミットの標準の `zero` 導出器では、上の `(members t)` に当たる箇所を `(eval (list 'members t))` としています。この版の `members` は受け取ったシンボルを型名として扱うため、変数 `t` の値を使って呼び出すには、このように呼び出し式を組み立てて評価します。[標準の導出器(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/core/Derive.carp#L86-L89)、[members の実装(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/src/Primitives.hs#L424-L443)

`make-deriver` は、関数定義と同じように読むと理解しやすくなります。インターフェース名は `zero` で、引数は取りません。型を受け取ったら、各メンバーに対する `zero` の呼び出しを生成し、全体を `init` で囲むだけで、その型の `zero` を定義できます。したがって、先ほどの `Point` 型に対する `zero` の定義は、次のようになります。

```clojure
(init (zero) (zero))
```

その周囲の定型コード (boilerplate) はすべて `derive` 自身が生成するため、`(derive Point zero)` という呼び出し全体は、次のように書き換えられます。

```clojure
(defmodule Point
  (defn zero []
    (init (zero) (zero)))
  (implements Point.zero zero)
)
```

> 訳注: 対象コミットの `make-deriver` が生成する `implements` は、インターフェース名、実装する関数名の順に引数を取ります。そのため、この例に対応する生成コードは `(implements zero Point.zero)` となり、原文の例とは引数順が逆です。[make-deriver の実装(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/core/Derive.carp#L25-L33)

つまり、導出器に必要なのは、型を受け取って関数本体を生成する方法だけです。また、引数の名前も導出器が決めるので、生成する定義の中でその引数を使うこともできます。

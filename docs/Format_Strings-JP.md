# 書式指定文字列 (Format Strings)

原文: [Format_Strings.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Format_Strings.md)

翻訳元のコミットは `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` です。
この文書は Carp の開発者・貢献者による英語原文を日本語に翻訳・編集した非公式の文書です。
翻訳方針は [TRANSLATION.md](../TRANSLATION.md)、採用語は [GLOSSARY.md](../GLOSSARY.md) を参照してください。

Carp には、文字列の書式を設定する方法が `fmt` と `fstr` の 2 つあります。この文書では、両方の関数を詳しく説明します。

## 書式の指定 (`fmt`)

`fmt` は `fstr` よりも細かく制御できますが、扱うデータについて、より詳しく知っている必要があります。

```clojure
(fmt "this is an integer %d and this is a string %s." 1 "hi")
```

C の [`printf`(英語)](https://en.wikipedia.org/wiki/Printf_format_string) と同じように動作します。`fmt` は、引数の数と、書式指定文字列 (format string) に含まれる書式指定子 (format specifier) の数が一致するかを検査します。

`fmt` に渡す引数の型はすべて、次のように定義される `unsafe-format` インターフェースを実装している必要があります。

```clojure
(definterface unsafe-format (Fn [String a] String))
```

> 訳注: 対象コミットの実際の定義は `(definterface unsafe-format (λ [&String a] String))` で、第 1 引数は `String` ではなく、その参照型 `&String` です。[インターフェースの定義(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/core/Interfaces.carp#L36)

各型の実装は、書式指定子を受け取り、それに従って書式を設定するものとされています。そのため、どの書式指定子に対応するかは、その型の `unsafe-format` の実装によって決まります。標準ライブラリの型では、C と同じ通常の書式指定子を利用できます。

また、`fmt` の書式指定文字列は、必ずリテラルでなければなりません。

## 単一の値の書式設定 (`unsafe-format`)

`unsafe-format` は、単一の値の書式を設定します。`snprintf` などの C 関数を呼び出す薄いラッパー (wrapper) で、名前が示すとおり安全ではありません。コンパイル時の検査を行わないため、変換指定 (directive) がちょうど 1 つ含まれる書式指定文字列でなければ、渡されていない引数を読み取ってしまいます。

```clojure
(Int.unsafe-format "%d%d" 1) ; 引数は 1 つ、変換指定は 2 つ
```

> 訳注: 原文の「ちょうど 1 つでなければ、渡されていない引数を読み取る」という説明には例外があります。例えば、変換指定を含まない通常の文字列では、余分な引数の値は使用されません。ただし、Carp の実行時検査は、`NDEBUG` を定義していなければ、この場合も変換指定の個数が不正として異常終了させます。[C の出力変換と引数(英語)](https://sourceware.org/glibc/manual/latest/html_node/Table-of-Output-Conversions.html)、[Carp の実行時検査(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/core/core.h#L27-L78)

`NDEBUG` を定義してビルドした場合を除き、どの `unsafe-format` 実装も、実行時に書式指定文字列を検査し、不一致があればプログラムを異常終了します。これは、配列の添字に境界検査を行うのと同様です。この検査は最後の備えであり、事前の検査の代わりにはなりません。コンパイル時に書式指定文字列を検査し、任意の個数の引数を扱える `fmt` を優先してください。

## 式の埋め込み (`fstr`)

`fmt` と同様に、`fstr` も文字列リテラルを受け取ります。ただし、使い方は `fmt` より単純で、式を文字列に直接埋め込み、`str` を使って書式を設定します。そのため、`fstr` 内のすべての式の返り値の型は、`str` インターフェースを実装している必要があります。

```clojure
(def x 1)
(def y "hi")

(fstr "this is an integer {x} and this is the first character of a string {(head x)}")
```

> 訳注: この例の `x` は整数ですが、説明文は文字列の先頭の文字を取り出す内容です。対象コミットの `fstr` のドキュメント文字列にある同様の例では、`(head y)` を使っています。ここも `(head y)` の誤記と考えられます。[実装内の使用例(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/core/Format.carp#L97-L107)

`fstr` には、構文解析可能な (parseable) 式なら何でも埋め込めます。式は `{}` で囲みます。単独の `}` は、その文字自体として扱われます。一方、文字としての `{` は、`{{` とエスケープする必要があります。

```clojure
(fstr "{{}") ; => {}
```

`fstr` 内に複雑な式や複数行にわたる式を埋め込むこともできますが、推奨しません。

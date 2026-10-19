# `drop` インターフェース (Drop)

原文: [Drop.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Drop.md)

翻訳元のコミットは `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` です。
この文書は Carp の開発者・貢献者による英語原文を日本語に翻訳・編集した非公式の文書です。
翻訳方針は [TRANSLATION.md](../TRANSLATION.md)、採用語は [GLOSSARY.md](../GLOSSARY.md) を参照してください。

Carp のどの型にも実装できる「特別な」インターフェースの 1 つが `drop` で、型シグネチャは `(Fn [&a] ())` です。その型の値への参照を受け取り、値が削除される前に実行されます。閉じる必要があるファイルなど、メモリを解放する前に特別な処理が必要な型のための仕組みです。

```clojure
(deftype A [])

(defmodule A
  (sig drop (Fn [(Ref A)] ()))
  (defn drop [a]
    (IO.println "Hi from drop!"))
)

(defn main []
  (let [a (A)]
    ()))
```

上の例では、`let` のスコープが終了するときに `A.drop` が実行され、`Hi from drop` が表示されます。

> 訳注: 原文の説明では `Hi from drop` としていますが、コード中の文字列は、末尾に `!` が付いた `Hi from drop!` です。

# マクロ (Macros)

原文: [Macros.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Macros.md)

翻訳元のコミットは `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` です。
この文書は Carp の開発者・貢献者による英語原文を日本語に翻訳・編集した非公式の文書です。
翻訳方針は [TRANSLATION.md](TRANSLATION.md)、採用語は [GLOSSARY.md](GLOSSARY.md) を参照してください。

どの Lisp でも、マクロは特に意見が分かれる機能の 1 つです。設計にあたっては多くの選択肢があり、それぞれに支持する人と反対する人がいます。

本書は、マクロシステムとその使い方を包括的に説明することを目指しています。急いでいる場合や、お気に入りのマクロ機能が Carp に実装されているかを知りたい場合は、[概要](#概要-in-a-nutshell) の節を読むとよいでしょう。マクロシステムの使い方や、その開発方法をじっくり理解したい場合は、[マクロの使い方](#マクロの使い方-working-with-macros) と [内部の仕組み](#内部の仕組み-inner-workings) の節が役に立つでしょう。

## 概要 (In a Nutshell)

Carp で採用したマクロシステムは、比較的単純です。次の特徴があります。

- 衛生的 (hygienic) ではありませんが、`gensym` の機能を提供します。
- 現時点では準クォート (quasiquoting) を提供しません。これは設計上の制約ではなく、単に未実装ということです。そのため、マクロを書く際に中心となる道具は `car`、`cdr`、`cons`、`list` です。
- 比較的単純な `defmacro` ベースの構文でマクロを定義し、コンパイル時の関数や動的関数もサポートします。この点について詳しくは、後述の [マクロの使い方](#マクロの使い方-working-with-macros) を参照してください。
- 動的環境 (dynamic environment) を、マクロ展開によってコードを生成するだけの環境ではなく、ソースについての追加情報をコンパイラに伝える場所としても扱います。例えば、動的関数 `Project.config` では、使用する C コンパイラ、コンパイルしたプロジェクトの名前、出力ディレクトリなどを設定できます。実際の例として、動的環境で複数のコンパイラを使う単純な Carp のビルドシステムを実装した [Carp のコード例(英語)](https://github.com/carpentry-org/snippets/blob/master/build_system.carp) を参照してください。

> 訳注: 翻訳元のコミットでは、標準のコアライブラリを読み込んだ動的コードで準クォートを利用できます。本節の「未実装」という説明は、この版の [準クォートの実装(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/core/Quasiquote.carp#L35-L90) と一致しません。使い方は、同じ固定版の [準クォート](Quasiquotation-JP.md) を参照してください。

## マクロの使い方 (Working with Macros)

マクロは、次のように `defmacro` というプリミティブ (primitive) の形式を使って定義します。

```clojure
(defmacro apply [f args] (cons f args))

(apply + (1 2)) ; => (+ 1 2)
(apply Array.replicate (5 "hello")) ; => (Array.replicate 5 "hello")
```

この例では、関数と、リストで表した実引数の集合を受け取るマクロ `apply` を定義しています。`f` を先頭、`args` を残りの要素とするリストを `cons` で構築し、その関数を実引数に適用する形に書き換えます。

`apply` はマクロなので、渡すリストをクォートする必要はありません。これが不自然に見えるなら、代わりに `apply` を動的関数として定義してもよいでしょう。マクロと動的関数の主な違いは、動的関数が実引数を評価することと、マクロが定義の内部で展開されることです。動的関数は、次のように定義できます。

```clojure
(defndynamic apply [f args] (cons f args))

(apply '+ '(1 2)) ; => (+ 1 2)
(apply 'Array.replicate '(5 "hello")) ; => (Array.replicate 5 "hello")
```

このコード例を先ほどのマクロの例と比べると、定義に `defndynamic` を使うことと、呼び出し時のクォートを除けば、非常によく似ていることが分かります。

マクロは残余引数 (rest arguments) もサポートします。つまり、最後の仮引数を、残りの実引数をすべて受け取るものとして指定すれば、可変長引数のマクロを定義できます。

```clojure
(defmacro apply-or-sym [head :rest tail]
  (if (= (length tail) 0)
    head
    (cons head tail)))

(apply-or-sym *global*) ; => *global*
(apply-or-sym + 1 2) ; => (+ 1 2)
```

`apply-or-sym` は少しばかばかしいマクロですが、説明したいことは伝わるはずです。このマクロは、まず `head` という仮引数を 1 つ取ります。その後には任意の個数の実引数を渡すことができ、それらは `tail` に束縛 (binding) されます。そのため、`tail` は 0 個以上の実引数を含むリストになります。実引数を追加しなければ、`apply-or-sym` はそのまま `head` を返します。追加した場合は、通常の関数呼び出しとして扱います。このようなマクロは少しおかしく見えるかもしれませんが、残余引数には実用的な用途がたくさんあります。

大小さまざまなマクロの例をもっと見たい場合は、ここまでの知識で、[標準ライブラリのマクロ(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/core/Macros.carp) の多くを理解できるはずです。かなり複雑なマクロの仕組みである [`fmt`(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/core/Format.carp) にも取り組めるでしょう。

REPL でマクロを調べる際には、`expand`、`eval`、`macro-log` が役に立ちます。`expand` はマクロを展開し、`eval` は得られたコードを評価します。`macro-log` は、マクロの処理を追跡する「printf デバッグ」に便利です。

## 内部の仕組み (Inner Workings)

Carp のコンパイラはいくつかの段階に分かれています。次の図は、コンパイラの処理の流れを示しています。

![コンパイラの処理段階(英語)](https://raw.githubusercontent.com/carp-lang/Carp/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/compiler-passes.svg)

動的評価器 (dynamic evaluator) は、Carp コンパイラの特に中心的な部分の 1 つといえます。関数定義、変数、`let` による束縛など、マクロ展開、借用チェック (borrow checking)、型推論を必要とする形式に遭遇すると、それらの処理を取りまとめます。

そのため、評価器を理解すれば、Carp 全体の仕組みについても多くのことが分かります。

現在の評価器を理解するうえでは、次の箇所から読み始めるとよいでしょう。

- [`src/Eval.hs`(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/src/Eval.hs) の `eval`。公開されているエントリーポイント (entrypoint) です。
- [`src/EvalIR.hs`(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/src/EvalIR.hs) の低水準化 (lowering)。
- [`src/EvalVM.hs`(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/src/EvalVM.hs) の VM 実行。

アーキテクチャの簡潔な概要については、[動的評価器 VM](EvaluatorVM-JP.md) を参照してください。

### データ構造 (Data Structures)

評価器の主なエントリーポイントは、次のとおりです。

```haskell
evalDynamic :: Context -> XObj -> IO (Context, Either EvalError XObj)
evalStatic  :: Context -> XObj -> IO (Context, Either EvalError XObj)
eval        :: Context -> XObj -> LookupPreference -> IO (Context, Either EvalError XObj)
```

これを理解するには、少なくとも `Context`、`XObj`、`EvalError` を理解する必要があります。`IO` と `Either` は Haskell の標準ライブラリに含まれる型なので、本書では詳しく説明しません。詳細については、好みの Haskell ドキュメント検索ツールを参照してください。お勧めは [Stackage(英語)](https://stackage.org) です。

ここで説明するデータ構造は、すべて [`src/Obj.hs`(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/src/Obj.hs) で定義されています。

#### `XObj`

`XObj` は「追加情報を持つ `Obj` (Obj with eXtras)」の略です。`Obj` は Carp の抽象構文木 (abstract syntax tree、AST) のノードを表す型で、コンパイラ全体で使われています。ただし、多くの場合は `XObj` に包まれた形で現れます。`XObj` は `Obj` に、省略可能なソース位置情報と型情報を付加します。ソース位置情報は `Maybe Info` 型の `info` フィールドに、型情報は `Maybe Ty` 型の `ty` フィールドに格納されます。どちらのフィールドも重要ですが、本書ではこれらを考慮せず、`XObj` を通常の AST ノードとして扱います。そのため、`eval` はコンテキスト (context) と AST ノードを受け取り、新しいコンテキストと、`EvalError` または新しい AST ノードとの組を返す関数と捉えられます。

#### `Context`

`Context` は、Carp コンパイラの状態をすべて保持するデータ構造です。型環境や値環境から、トレースバック (traceback) のために記録する評価フレーム (evaluation frame) の履歴まで、幅広い情報を保持します。

コンパイラの状態は、すべてコンテキストを調べることで確認できるはずです。

#### `EvalError`

動的評価器がエラーに遭遇すると、`EvalError` が生成されます。これは、エラーメッセージと、トレースバックやソース位置情報などのメタ情報で構成されます。

### 評価 (Evaluation)

Carp の動的評価器は、評価だけでなく、定義などのメタレベルの情報も扱います。つまり、定義は特別な構文要素というより、評価対象となる動的なプリミティブと同じように扱われます。実際、その多くは特殊形式としてではなく、`Primitive` として実装されています。

すでにいくつかの構文要素の名前を挙げたので、評価器が扱う Carp の構文要素を分類します。

- 特殊形式 (special forms): 抽象構文木の中に専用の表現を持ち、評価器のループ内で直接処理される形式です。`fn` や `the` がこの分類に当たります。高階関数 (higher order functions) で行うように、値として受け渡すことはできません。
- プリミティブ: 実引数を評価しない、通常の Carp の形式です。Haskell で実装された組み込みマクロに似ています。`defmacro`、`defn`、`quote` がこの分類に当たります。
- コマンド (commands): これらも通常の Carp の形式です。実引数を評価し、組み込み関数のように振る舞います。`Project.config`、`car`、`cons` がこの分類に当たります。

> 訳注: 翻訳元のコミットの `defn` は、専用の `Defn` 表現を持つ特殊形式です。実引数を通常の関数のように事前評価しない点は共通ですが、[初期環境への登録(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/src/StartingEnv.hs#L479-L505) では `Defn Nothing` として登録されます。そのため、本節の実装上の分類で、[`defmacro`・`quote`(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/src/StartingEnv.hs#L299-L324) と同じ `Primitive` の例に挙げる説明は不正確です。

プリミティブは主に [`src/Primitives.hs`(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/src/Primitives.hs) で定義され、コマンドは [`src/Commands.hs`(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/src/Commands.hs) にあります。特殊形式は、評価器の低水準化・実行処理 (`EvalIR` / `EvalVM`) で扱われます。

これらは [`src/StartingEnv.hs`(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/src/StartingEnv.hs) で環境に登録され、名前が付けられます。

#### 独自の特殊形式、プリミティブ、コマンドの追加 (Adding your own special forms, primitives, or commands)

独自のプリミティブやコマンドを Carp の評価器に追加するには多くの仕組みが関わりますが、実装を始める際に役立つ単純な関数もたくさん用意されています。

プリミティブやコマンドと同じ名前の関数が実行時の関数としてすでに存在する場合は、その振る舞いにできるだけ近づけるべきです。

特殊形式の追加はもう少し複雑です。形式を追加するたびに `eval` を理解してその動作を考えることが難しくなるため、何を追加するかは慎重に判断しています。新しい特殊形式の実装に取りかかる前に、無駄な苦労を避けるためにも [チャット(英語)](https://gitter.im/carp-lang/carp) で相談するとよいでしょう。

> 訳注: このチャットは Carp 本体への機能追加を相談する場所です。日本語訳や訳注の問題は、本家ではなく [このリポジトリの Issue](https://github.com/oz-coden/carp-language-documents-for-japanese/issues) へ報告してください。翻訳の問題か原文の問題か判断できない場合も、まずこちらへ相談してください。

#### 現在の特殊形式の一覧 (A current list of special forms)

特殊形式は「魔法のような」ものなので、一覧にしておきます。これらは評価器の低水準化・実行処理で認識されます。現在は次のものがあります。

- `if`: 分岐。
- `defn`: 関数の定義。
- `def`: グローバル変数の定義。
- `let`: 局所変数の定義。
- `the`: 型注釈。
- `fn`: 関数リテラル。

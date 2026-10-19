# 動的意味論 (Dynamic Semantics)

原文: [DynamicSemantics.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/DynamicSemantics.md)

翻訳元のコミットは `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` です。
この文書は Carp の開発者・貢献者による英語原文を日本語に翻訳・編集した非公式の文書です。
翻訳方針は [TRANSLATION.md](../TRANSLATION.md)、採用語は [GLOSSARY.md](../GLOSSARY.md) を参照してください。

本書は、Carp の動的評価器 (dynamic evaluator) を書き直す際に掲げていた、過去の目標を説明する文書です。

その後、評価器は VM を基盤とするアーキテクチャへ移行しました。現在の実装については、[動的評価器 VM](EvaluatorVM-JP.md) を参照してください。

## 書き直しの目標 (Goals of the rewrite)

- 動的評価に関して見つかったさまざまなバグを修正します。下記の「関連する Issue」を参照してください。
- 動的な Lisp なら備えていると期待される、未実装の機能を追加します。下記を参照してください。
- 将来、動的評価器に新しい機能を追加しやすくします。

## 関連する Issue (Relevant issues)

- [#560(英語)](https://github.com/carp-lang/Carp/issues/560)
- [#555(英語)](https://github.com/carp-lang/Carp/issues/555)
- [#545(英語)](https://github.com/carp-lang/Carp/issues/545)
- [#476(英語)](https://github.com/carp-lang/Carp/issues/476)
- [#556(英語)](https://github.com/carp-lang/Carp/issues/556)
- [#659(英語)](https://github.com/carp-lang/Carp/issues/659)
- [#660(英語)](https://github.com/carp-lang/Carp/issues/660)
- [#453(英語)](https://github.com/carp-lang/Carp/issues/453)

## 希望する機能 (当時は未実装) (Desired features (currently missing))

- 動的言語とマクロシステムの使い方を説明する文書。
- 完全なマクロ機能。準クォート (quasiquoting)、スプライシング (splicing)、十分なエラー報告などを含みます。
- 動的なスタックトレース (stack trace)。
- ユーザー定義名の自動補完。

<hr>

## 目次 (Index)

[TODO]

## 0. 本書で使用する用語 (0. Terms used in this document)

- 形式 (form): テキストで表現された、有効な Carp のデータ構造です。
- トップレベル (top level): 他の形式の内部に含まれていない形式です。
- 静的 Carp (Static Carp): コンパイルされる版の Carp 言語です。
- 動的 Carp (Dynamic Carp): 解釈実行される、関数型で、GC によるメモリ管理を行う版の Carp 言語です。

## 1. スコープの規則 (1. Scoping Rules)

関連する Issue:

- [#659(英語)](https://github.com/carp-lang/Carp/issues/659)

質問:

#### Carp はシンボル X の値をどのように決定しますか？ (How does Carp figure out what the value of the symbol X is?)

字句スコープ (lexical scoping) に従います。現在のスコープから、それを囲むスコープへと順に調べ、グローバルスコープまでたどります。
スコープを作るものは次のとおりです。

- 関数定義 (`defn`、`defndynamic`、`fn`)
- `let`
- モジュール

#### シンボル X の値を設定するにはどうしますか？ (How do you set the value for symbol X?)

`(set! <symbol> <value>)`

#### 予約名はありますか？ (Are there any reserved names?)

はい。予約名 (reserved names) は次のとおりです。詳しくは `Parsing` モジュールを参照してください。

- `defn`
- `def`
- `do`
- `while`
- `fn`
- `let`
- `break`
- `if`
- `match`
- `true`
- `false`
- `address`
- `set!`
- `the`
- `ref`
- `deref`
- `with`

実際には、ほかにも予約名の一覧へ移すべきものがあります。
`defmacro` の `:rest` トークンも予約されています。

#### キーワードとは何ですか？ (What is a keyword?)

キーワードはありません。マクロでは導入されるかもしれません。[こちらの実装例(英語)](https://gist.github.com/sdilts/73a811a633bb0ef3dd7e31b84a138a5a) を参照してください。

#### 動的 Carp と静的 Carp には、それぞれ別の名前空間がありますか？ (Are there different namespaces for dynamic and static Carp?)

同じモジュールを使いますが、動的な名前解決では動的関数だけが見つかり、静的な名前解決では静的関数だけが見つかります。

### 1.1 グローバル変数 (1.1 Global Variables)

質問:

#### グローバル変数は変更できますか？ (Are global variables mutable?)

はい。

#### どのように変更し、変更はいつ反映されますか？ (How are they mutated? When do these mutations come into affect?)

`set!` を使います。変更はすぐに反映されます。内部では `IORef` を使います。

#### グローバル変数は字句スコープと動的スコープのどちらに従いますか？ (Do global variables have lexical or dynamic scope?)

字句スコープです。どの要素にも動的スコープ (dynamic scope) はありません。

### 1.2 局所変数 (1.2 Local variables)

質問:

#### 局所変数は変更できますか？ (Are local variables mutable?)

はい。

#### 局所変数はいつスコープに入り、いつ外れますか？ (When do local variables come in and out of scope?)

字句スコープの規則に従います。関数と `let` が新しい変数を作ります。

#### クロージャとは何ですか？ クロージャ内の変数について、どの規則が重要ですか？ (What is a closure? What are the important rules for variables inside closures?)

キャプチャした変数は、いずれも変更できません。
動的なラムダ (lambda) は、クロージャ (closure) を生成した時点、つまり `(fn ...)` 形式を評価した時点の環境全体をキャプチャします。

### 1.3. 名前空間の規則 (1.3. Namespace Rules)

質問:

#### `Foo` モジュールのシンボル `a` と `Bar` モジュールのシンボル `a` を、それぞれどのように参照しますか？ (Given symbols `a` in the `Foo` module and `a` in the `Bar` module, how do I refer to each of them?)

`.` を使い、`Foo.a` と `Bar.a` のように参照します。
`(use <module name>)` を使うと、モジュールを指定する手間を省けます。

#### 複数のモジュールをインポートし、それらに同じシンボルが含まれていると、どうなりますか？ (What happens if multiple modules are imported and they contain the same symbol?)

そのシンボルを名前解決するときに、実行時エラーになります。

#### `Foo.a` と `Bar.a` が存在するとき、`a` はどちらを参照しますか？ (Given the symbols`Foo.a` and `Bar.a`, exist, which symbol does `a` refer to?)

どちらも参照しません。ただし、どちらか一方のモジュール (`Foo` または `Bar`) だけを `use` でインポートした場合は、そのモジュールのシンボルを参照します。両方をインポートすると、単一の値に解決できないため、名前解決時にエラーになります。

#### 関数と変数は同じ名前空間に属しますか？ (Do functions and variables live in the same namespace?)

はい。型は別の名前空間 (namespace) に属します。

### 1.4 定義 (1.4 Definitions)

質問:

#### どのような種類の定義があり、それぞれどのように作成しますか？ (What kinds of definitions are there and how are they created?)

動的なコンテキスト (context):

- `defndynamic`: 動的関数を作成します。
- `defdynamic`: 動的なグローバル変数を作成します。
- `defmacro`: マクロを作成します。

静的なコンテキスト:

- `defn`: 静的関数を作成します。
- `def`: 静的なグローバル変数を作成します。
- `deftype`: 直積型 (product type) と直和型 (sumtype) を定義します。
- `register`: 外部関数を利用できるようにします。

すべてのコンテキスト:

- `defmodule`

## 2. 評価規則 (2. Evaluation Rules)

関連する Issue:

- [#555(英語)](https://github.com/carp-lang/Carp/issues/555)

質問:

#### マクロはいつ評価されますか？ (When are macros evaluated?)

#### シンボルはいつ評価されますか？ (When are symbols evaluated?)

#### 形式はいつ評価されますか？ (When are forms evaluated?)

#### 形式は左から右と右から左のどちらの順に評価されますか？ (Are forms evaluated left-to-right or right-to-left?)

#### エラー報告はどのように行われますか？ (How does error reporting work?)

### 2.1 マクロ (2.1 Macros)

質問:

- マクロとは何ですか？
- マクロ展開時には、どの関数を使えますか？
- 準クォートとは何ですか？ どのような構文を使いますか？
- スプライシングとは何ですか？ どのような構文を使いますか？

### 2.2 REPL (2.2 REPL)

質問:

- REPL は、何かを動的なコンテキストと静的なコンテキストのどちらで評価するかを、どのように判断しますか？
- 渡されたコードを動的なコンテキストと静的なコンテキストのどちらで実行するかは、いつ決まりますか？

## 3. 型 (3. Types)

Issue:

- [#560 リフレクション (Reflection) モジュールの追加提案(英語)](https://github.com/carp-lang/Carp/issues/560)

質問:

- どのような型を使えますか？
- 形式の型チェックはいつ行われますか？
- 特定の型をどのように参照しますか？ 型は [第一級オブジェクト (first class citizens)(英語)](https://en.wikipedia.org/wiki/First-class_citizen) ですか？

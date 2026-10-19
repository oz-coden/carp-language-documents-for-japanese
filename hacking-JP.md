# Carp コンパイラの開発 (Hacking the Carp Compiler)

原文: [hacking.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/hacking.md)

翻訳元のコミットは `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` です。
この文書は Carp の開発者・貢献者による英語原文を日本語に翻訳・編集した非公式の文書です。
翻訳方針は [TRANSLATION.md](TRANSLATION.md)、採用語は [GLOSSARY.md](GLOSSARY.md) を参照してください。

この文書には、Carp コンパイラに変更を加える際に役立つ、さまざまなヒントや工夫、メモ、説明、例をまとめています。網羅的なガイドではありません。今後も、過去にコンパイラを変更した人たちによるコメント、観察、ヒントを寄せ集めたものになっていくでしょう。

> 注: コンパイラとコンパイルに関する用語について、一般的な知識があることを前提としています。

## 構成 (Structure)

Carp コンパイラのソースコードは、`src/` ディレクトリにあります。大まかにいうと、Carp は 4 つの主要なパス (pass)、またはコンポーネントで構成されています。

![Carp コンパイラの処理段階(英語)](https://raw.githubusercontent.com/carp-lang/Carp/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/compiler-passes.svg)

各ソースファイルは、コンパイラの 1 つ以上のコンポーネントや処理段階で役割を担っています。以下の節では、各段階の目的を簡単に説明し、重要なソースファイルを挙げます。ある処理段階の機能を変更する際に、どのファイルを編集すればよいか、おおよその見当を付けるために使えます。

> 注: コンパイラのほぼすべての処理段階で重要、または使用される定義を含むソースファイルもあります。そのため、以下の複数の節に同じファイルが登場することがあります。

### 構文解析 (Parsing)

構文解析 (parsing) の段階では、`.carp` ソースファイルを抽象構文木 (abstract syntax tree、AST) に変換します。Carp では、AST のノードを `XObj` という抽象データ型 (abstract data type) で表します。`XObj` はコンパイラ全体で広く使われ、複数の処理段階や文脈で利用されます。各 `XObj` は、次の要素で構成されます。

- `Obj`: Carp のソースコードを抽象データ型として表現したものです。
- `Info`: `Obj` の生成元となったソースコードについての追加情報を保持します。例えば、ソースファイル内の位置です。
- `Ty`: [型システム](#型システム-type-system) が決定した、`Obj` に対する有効な Carp の型です。

> 訳注: 対象コミットの `XObj` では、情報と型のフィールドはそれぞれ `Maybe Info` と `Maybe Ty` であり、省略可能です。したがって、すべてのノードに有効な型情報がすでに付いているとは限りません。[XObj の定義(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/src/Obj.hs#L342-L347)

構文解析では、次のソースファイルが重要です。

- `Parsing.hs`: Carp のソースコードを抽象構文に変換する構文解析処理です。
- `XObj.hs`: 有効な Carp の AST ノードを定義します。

> 訳注: 対象コミットに `src/XObj.hs` は存在しません。`Obj` と `XObj` は [Obj.hs(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/src/Obj.hs#L129-L174) と [同ファイルの XObj 定義(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/src/Obj.hs#L342-L347) で定義されています。

### 動的評価器 (Dynamic Evaluator)

[マクロガイド](Macros-JP.md#内部の仕組み-inner-workings) で述べているように、動的評価器 (dynamic evaluator) はコンパイラの中心となるコンポーネントです。名前のとおり、構文解析された Carp コード (`XObjs`) を評価し、[コード出力 (emission)](#コード出力-code-emission) に向けて準備します。評価には、次の処理が含まれます。

- マクロと動的関数の展開
- ほかの形式への束縛 (binding) の解決
- 形式に対する型推論の要求
- 形式に対する借用チェック (borrow checking) の要求

評価器は、コンパイルするソースファイルに対応する `XObjs` に加えて、`Context` も使用します。`Context` は、コンパイラの状態を保持するグローバルなオブジェクトで、コンテキスト (context) を表します。コンパイラの `Context` は、`Env` 型で定義される複数の環境から構成され、それぞれが既知の束縛への参照を保持します。コンパイラの各処理段階では、異なる環境を使って形式の評価や型の解決を行い、大まかにいうと、コード出力に向けた準備を進めます。

`Binders` も、評価で使われる重要な抽象データ型です。ソースプログラム内で名前に束縛された値は、`binder` に変換されます。これは、その名前に束縛された形式の `XObj` と、その束縛についての追加のメタデータ (metadata) で構成されます。`Binders` は、`Context` 内の環境に追加されます。

評価では、次のソースファイルが重要です。

- `Eval.hs`: 評価器の公開エントリーポイント (entry point) です。
- `EvalIR.hs`: 評価器の中間表現 (IR) と、`XObj` からの低水準化 (lowering) を扱います。
- `EvalVM.hs`: 評価器 VM (evaluator VM) のコンパイル・実行経路 (`runEvalIRVM`) を扱います。
- `EvalCode.hs` / `EvalVMCore.hs`: 評価器のバイトコード (bytecode) と、VM の低水準の実行処理を扱います。
- `Obj.hs`: `Env` の形で評価の各パスにわたるコンパイラの状態を保持する `Context` と、名前から `XObjs` への対応を表す `Binders` を保持する `Env` を定義します。
- `Primitives.hs`: 引数を評価 **しない** 組み込み関数、または「キーワード」です。
- `Commands.hs`: 引数を評価する組み込み関数、または「キーワード」です。
- `StartingEnv.hs`: コンパイラが使う初期環境を定義します。評価の各パスが使えるように、すべてのコマンド (commands) とプリミティブ (primitives) をここで登録します。
- `Lookup.hs`: 与えられた環境 (`Env`) から `Binders` を検索する関数です。
- `Expand.hs`: 形式を走査し、構文の解析 (syntactic analysis) を行う関数です。以前はマクロ展開も行っていましたが、その機能は `Eval.macroExpand` に移されました。
- `Infer.hs`: 型推論を行う関数で、型システムへの入口です。
- `Qualify`: 適切なモジュール名でシンボルを修飾します。

> 訳注: 対象コミットに `src/Lookup.hs` は存在しません。コンテキスト内の束縛を検索する処理は、例えば [Context.hs の lookupBinderInContextEnv(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/src/Context.hs#L353-L369) にあります。

型システムや借用チェックの仕組みの一部を、この一覧に加えることもできるでしょう。ただし、ここでは評価に関わる中核機能を挙げています。大まかにいえば、評価コンポーネントはコンパイルという交響曲の指揮者であり、コンパイラのほかのすべての部分をまとめて動かします。

> 注: 動的評価器をさらに詳しく知りたい場合は、[マクロガイドの内部の仕組みの節](Macros-JP.md#内部の仕組み-inner-workings) と [動的評価器 VM](EvaluatorVM-JP.md) を参照してください。

### 型システム (Type System)

型システムは、Carp の形式の型を検査し、プログラムの型安全性を保証する役割を担います。多相性 (polymorphism) も扱い、多相型 (polymorphic type) を具体的な型 (concrete type) に置き換えます。

Carp の型は、`Ty` データ型で表します。

型システムでは、次のソースファイルが重要です。

- `Types.hs`: 有効な Carp の型を表す `Ty` データ型を定義します。2 つの型に互換性があるかどうかを判断する、単一化 (unification) の検査コードも含みます。また、Carp の型名を有効な C の識別子に変換する名前マングリング (mangling) のコードも含みます。
- `TypeError.hs`: 型検査のエラーを定義します。
- `AssignTypes.hs`: 変数に具体的な型を割り当てます。
- `Polymorphism.hs`: 具体化 (concretization) された多相関数 (polymorphic function) に対し、その具体的な関数に対応する正しい有効な C の識別子を決定します。
- `Validate.hs`: ユーザー定義型が有効であることを検査します。
- `Constraints.hs`: 環境内の型と型変数の間の制約 (constraint) を決定し、解きます。
- `Concretize.hs`: 多相型を含む形式を、具体的な型を使う形式に変換します。
- `InitialTypes.hs`: 与えられた `XObj` (AST ノード) の初期の型を決定します。
- `GenerateConstraints.hs`: 与えられた形式の型制約を決定します。

### 借用チェックと所有権システム (Borrow Checking/Ownership System)

借用チェックとライフタイムパラメーター (lifetime parameter) は、[型システム](#型システム-type-system) の拡張です。型システムで重要なファイルはすべて、借用チェッカー (borrow checker) にとっても重要です。

### コード出力 (Code Emission)

コンパイラの最後の仕事は、入力された Carp のソースコードに対応する C コードを出力することです。コード出力は、`Templates` という概念に大きく依存します。これは実質的には、評価済みの Carp の AST ノードに基づいて C のコード文字列を生成する、構造化されたテンプレート (template) の仕組みです。

コード出力システムでは、次のソースファイルが重要です。

- `ArrayTemplates.hs`: Carp での `Array` の利用に対応する C コードのテンプレートです。
- `StaticArrayTemplates.hs`: Carp での `StaticArray` の利用に対応する C コードのテンプレートです。
- `Deftype.hs`: Carp のユーザー定義の構造体、つまり直積型 (product type) に対応する C コードのテンプレートです。そのような型の束縛を登録する処理なども含みます。
- `Sumtypes.hs`: Carp のユーザー定義の直和型 (sumtype) に対応する C コードのテンプレートです。そのような型の束縛を登録する処理なども含みます。
- `StructUtils.hs`: Carp の構造体の補助関数に対応する C コードのテンプレートです。
- `Template.hs`: C コードを生成するための、コンパイラへの汎用的な指示を扱います。
- `ToTemplate.hs`: C コードの文字列からテンプレートを作成するための補助処理です。
- `Scoring.hs`: 型付けの情報と `XObj` の情報に基づき、出力される C の束縛の適切な並び順を決定します。
- `Emit.hs`: 評価・コンパイル済みの Carp のソースコードに基づき、生成された C コードを出力します。

### その他のソースファイル (Other sources)

上記のソースファイルに加えて、コンパイラ内でさまざまな役割を果たすファイルがあります。

- `Repl.hs`: キーワード補完や REPL のコマンドなど、REPL の機能を定義します。
- `Util.hs`: さまざまな補助関数です。
- `ColorText.hs`: REPL やコンパイラの出力を色付きにする機能です。
- `Path.hs`: ファイルパスを操作する関数です。
- `RenderDocs.hs`: 注釈を付けた Carp コードからドキュメントを生成する機能です。

## 短い実践ガイド (Mini HowTos)

コンパイラに加える変更の中には、ほかの変更よりも頻繁に行われ、大まかな手順が共通しているものがあります。以下の節では、そのような変更について案内します。

### 新しいプリミティブの追加 (Adding a new Primitive)

特殊な処理や変わった仕組みが必要でなければ、コンパイラに新しいプリミティブを追加する手順は次のとおりです。

1. `Primitives.hs` に新しいプリミティブを定義します。
2. `StartingEnv.hs` の `makePrim` を使って、プリミティブを初期環境に追加します。

#### プリミティブを定義する (Define your Primitive)

プリミティブは、`Primitive` 型の関数です。

```
type Primitive = XObj -> Context -> [XObj] -> IO (Context, Either EvalError XObj)
```

> 訳注: 対象コミットでは、この関数型は `VariadicPrimitiveCallback` という名前で定義され、引数の個数別にコールバック型が分かれています。`Primitive` は、この型の別名ではなく `Obj` のコンストラクタです。引数の個数別のコールバックは `PrimitiveFunctionType` でまとめて表します。[プリミティブの表現(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/src/Obj.hs#L170)、[コールバック型の定義(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/src/Obj.hs#L258-L277)

各プリミティブは、プリミティブ自身を表す形式である `xobj`、コンパイラのコンテキスト、そのプリミティブの形式に渡された実引数を表す `XObj` のリストを受け取ります。プリミティブは、行った処理に基づいて更新した新しい `Context` と、`XObj` または利用者に報告する評価エラーとの組を返します。

例えば、`defmodule` プリミティブと `Primitive` 型との対応は、次のようになります。

```
(defmodule Foo (defn bar [] 1))
 |         |-----------------|
 XObj      [XObj] (実引数)
```

> 引数 `Context` はコンパイラの状態を保持し、Carp の形式の中に直接対応する表現はありません。

`Primitives.hs` では、`primitive<name>` という命名規則でプリミティブに名前を付けてください。`<name>` は、Carp コードでそのプリミティブを呼び出すシンボルの名前です。例えば、`defmodule` に対応するプリミティブは `primitiveDefmodule` です。

ほとんどの場合、プリミティブの処理は、次の 3 つの主要な手順で構成されます。

- 実引数の `XObj` に対してパターンマッチングを行う
- 現在の `Context` から既存の束縛を検索する
- 実引数の `XObj` の種類に応じた処理を行い、必要に応じて `Context` を更新する

単純な `immutable` プリミティブを実装しながら、各手順を順番に見ていきます。このプリミティブは、変数、つまり `def` に渡した形式の名前を受け取り、それを不変 (immutable) としてマークします。それに対する `set!` の呼び出しを防ぐことが目的です。

- 手順 1. 実引数に対してパターンマッチングを行います。

  まず、Carp コードでのプリミティブの形は、次のようにします。

  ```
  (immutable my-var)
  ```

  つまり、このプリミティブが受け取る実引数の `XObj` は 1 つだけで、その実引数は `Sym` である必要があります。

  パターンマッチングを行ってみます。

  ```
  primitiveImmutable :: Primitive -- 新しいプリミティブ
  primitiveImmutable xobj ctx [XObj (Sym path@(SymPath) _)] =
    -- TODO: ここに実装する！
  primitiveImmutable _ _ xobjs = -- これ以外の個数や型の xobj 引数は不正なので、エラーにする
    return $ evalError ctx ("`immutable` expected a single symbol argument, but got" ++ show xobjs) (info xobj)
  ```

  これで、パターンマッチングに必要な処理は終わりです。

- 手順 2. 現在のコンテキストから束縛を検索します。

  `immutable` が正しい実引数を受け取ったとすると、次は受け取った `Sym` の `XObj` を使って、そのシンボルが変数に束縛されているかどうかを調べます。

  `Lookup.hs` は、コンテキストに含まれるさまざまな環境から束縛を検索する関数を定義しています。検索関数を呼び出し、受け取ったシンボル引数が `def` 形式に束縛されているか、つまり変数であるかを検査します。シンボルが `def` に束縛されていなければ、エラーにします。

  そこで、実引数に対応する束縛 (`Binder`) を取得し、その束縛の `XObj` に対してパターンマッチングを行い、`def` の場合だけ処理を続けます。

  ```
  primitiveImmutable :: Primitive -- 新しいプリミティブ
  primitiveImmutable xobj ctx [XObj (Sym path@(SymPath) _)] =
    let global = contextGlobalEnv ctx
        binding = lookupInEnv path global
    in  case binding of
          Just (_, Binder meta (XObj )) -> -- TODO: def であることが分かったので、ここで処理を続ける
          _ -> -- def でないものはエラーにする
            return $ evalError ctx ("`immutable` expects a variable as an argument") (info xobj)
  primitiveImmutable _ _ xobjs = -- これ以外の個数や型の xobj 引数は不正なので、エラーにする
    return $ evalError ctx ("`immutable` expected a single symbol argument, but got" ++ show xobjs) (info xobj)
  ```

- 手順 3. 処理を行い、`Context` を更新します。

  最後に、`def` であることが確認できたので、独自の処理を行い、変更した束縛でコンテキストを更新します。

  単純にするため、このプリミティブでは、束縛の `MetaData` に `immutable` というキーを追加し、その値を `true` にするだけにします。あとで、このメタデータのフィールドの値を使って、`set!` の呼び出しを防ぐことができます。

  ```
  primitiveImmutable :: Primitive -- 新しいプリミティブ
  primitiveImmutable xobj ctx [XObj (Sym path@(SymPath) _)] =
    let global = contextGlobalEnv ctx
        binding = lookupInEnv path global
    in  case binding of
          Just (_, Binder meta def@(XObj Def _ _)) ->
            let oldMeta = getMeta meta
                newMeta = meta {getMeta = Map.insert "immutable" trueXObj oldMeta}  -- 束縛のメタデータを更新する
            in  return $ ctx {contextGlobalEnv = Env (envInsertAt global path (Binder newMeta def))} -- 束縛と新しいメタデータでコンテキストを更新し、返す
          _ -> -- def でないものはエラーにする
            return $ evalError ctx ("`immutable` expects a variable as an argument") (info xobj)
  primitiveImmutable _ _ xobjs = -- これ以外の個数や型の xobj 引数は不正なので、エラーにする
    return $ evalError ctx ("`immutable` expected a single symbol argument, but got" ++ show xobjs) (info xobj)
  ```

> 訳注: 上の例は、固定版にそのまま組み込める完成例ではありません。`XObj` は 3 フィールド、`SymPath` は 2 フィールドですが、例のパターンでは不足しています。また、フォールバック節では `ctx` と `xobj` を束縛せずに参照しています。原文のコード断片は、これらを補完せず掲載しています。[XObj の定義(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/src/Obj.hs#L342-L347)、[SymPath の定義(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/src/SymPath.hs#L18-L19)

これで、プリミティブの中核となる処理は完成です。利用できるようにするには、あとは `StartingEnv.hs` に登録するだけです。

#### プリミティブを初期環境に追加する (Add your primitive to the starting environment)

プリミティブを初期環境に追加するには、`makePrim` を呼び出します。

```
, makePrim "immutable" 1 "annotates a variable as immutable" "(immutable my-var)" primitiveImmutable
```

> 訳注: 対象コミットの `makePrim` は、`SymPath`、`PrimitiveFunctionType`、説明文、使用例の 4 引数をこの順に受け取ります。上の呼び出し形式とは一致しません。単項プリミティブ用の `makeUnaryPrim` も用意されています。[makePrim の定義(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/src/Primitives.hs#L64-L89)、[makeUnaryPrim の定義(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/src/Primitives.hs#L45-L46)

手順はおおむね以上です。この実装は、束縛に特別なメタデータを追加するだけであることに注意してください。不変とした `def` に対する `set!` の呼び出しを実際に防ぐには、`set!` の処理を変更し、`immutable` メタデータの有無を検査する必要があります。

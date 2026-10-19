# コンパイラマニュアル (The Compiler Manual)

原文: [Manual.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Manual.md)

翻訳元のコミットは `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` です。
この文書は Carp の開発者・貢献者による英語原文を日本語に翻訳・編集した非公式の文書です。
翻訳方針は [TRANSLATION.md](TRANSLATION.md)、採用語は [GLOSSARY.md](GLOSSARY.md) を参照してください。

## 関連文書 (Related pages)

- [インストール](Install-JP.md): Carp コンパイラの入手方法と設定方法です。
- [コードの実行方法](HowToRunCode-JP.md): `.carp` ファイルをコンパイルして実行する方法です。
- [開発ツール(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Tooling.md): 対応するエディターを紹介しています。
- [ライブラリ](Libraries-JP.md): ライブラリとモジュールの利用方法です。
- [マルチメディア(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Multimedia.md): グラフィックスやサウンドなどを扱います。
- [マクロ(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Macros.md): Carp のマクロシステムのガイドです。
- [組み込み開発(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Embedded.md): 組み込みシステムで Carp を使うためのヒントや工夫です。
- [用語(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Terminology.md): よく使う用語と、それらが意味するものを説明しています。

Carp 言語やその構文、意味論について詳しく知るには、[Carp 言語ガイド](LanguageGuide-JP.md) を参照してください。

## REPL の基本 (REPL Basics)

Carp 言語は REPL と非常に密接に統合されており、プログラムに対して行いたい操作は、すべてここから制御できます。

ディスクからコードを読み込むには `(load "filename.carp")` を使います。これにより、ソースファイル `filename.carp` が現在の「プロジェクト」に追加されます。プロジェクトは、Eclipse や Visual Studio などの IDE と同じように、ソースファイルとコンパイラの設定をまとめる、REPL 内の軽量な概念です。

現在のプロジェクトをビルドするには、`(build)` を呼び出します。`main` 関数を定義しているかどうかに応じて、実行ファイルまたは動的ライブラリ (dynamic library) が生成されます。ライブラリを生成するプロジェクトでは、グローバル変数が自動では初期化されないことに注意してください。ライブラリの利用側で、C の関数 `carp_init_globals` または Carp の関数 `System.carp-init-globals` を呼び出す必要があります。

コンパイラが生成したものは、既定ではすべて `out` というディレクトリに保存されます。この設定を含め、プロジェクトに関する設定は各種コマンドで変更できます。利用できるコマンドの一覧を見るには、`(help "project")` を呼び出します。

REPL でよく行う操作には、便利なショートカットがあります。

```
:r   プロジェクトのすべてのファイルを再読み込みする
:b   プロジェクトをビルドする
:x   実行ファイルを実行する (存在する場合)
:c   生成された C コードを見る
:e   すべての関数の束縛 (binding) とその型を含む環境を表示する
:p   プロジェクトの情報と設定を表示する
:h   ヘルプ画面を表示する
:q   REPL を終了する
```

## ほかの Lisp の REPL との違い (Differences compared to REPL:s in other Lisp:s)

Carp の REPL は強力ですが、現時点では、ほかの多くの Lisp と比べて大きな制限がいくつかあります。式を入力して Enter キーを押すと、次のいずれかが起こります。

1. 動的関数 (`defndynamic` で定義したもの、または組み込みの `command`) を呼び出した場合は、Carp の動的評価器 (dynamic evaluator) がすぐに実行します。動的評価器は、内部の評価器 VM (evaluator VM) として実装されています。動的関数は、コンパイルされるコードでは使えません。主な用途は、マクロと、ビルド設定をプログラムから制御することです。
2. `defn` で定義した関数を呼び出した場合は、「通常の」Carp 関数として C を経由して実行可能なバイナリにコンパイルされ、REPL の子プロセス (child process) として実行されます。つまり、その関数は、グローバル変数など、プログラム内のほかのものを変更できません。
3. トップレベルの形式が関数呼び出しではない場合、REPL がうまく処理できないことがあります。例えば、Carp の関数への呼び出しを含む配列を入力すると、予期しない結果になります。配列は動的ですが、関数呼び出しは動的ではないためです。現時点で最も簡単な回避策は、式を `defn` で包み、代わりにその関数を呼び出すことです。この問題は Carp の今後のバージョンで修正される予定です。

## 注釈の追加 (Adding annotations)

Carp には、Clojure の仕組みから着想を得た柔軟なメタデータ (metadata) システムがあります。環境内の束縛に対して、誰でもデータを追加・取得できます。一般には、`(meta-set! <path> <key> <value>)` と `(meta <path> <key>)` を使います。

この仕組みの上に、便利なマクロがいくつか実装されています。

```clojure
(doc <path> "This is a nice function.") ; ドキュメント
(sig <path> (Fn [Int] Bool))            ; 型注釈
(private <path>)                        ; 関数をほかのモジュールからアクセスできなくする
```

これらの例では、`<path>` はいずれも `foo` や `Game.play` などのシンボルであることに注意してください。

ドキュメント文字列 (doc strings) から HTML ドキュメントを生成するには、次を実行します。

```clojure
(save-docs <module 1> <module 2> <etc>)
```

## 束縛の型の取得 (Getting types from bindings)

```clojure
鲮 (type <binding>)
鲮 :t <binding>
```

## モジュール内の束縛の一覧表示 (Listing bindings in a module)

```clojure
鲮 (info <module name>)
鲮 :i <module name>
```

## マクロの展開 (Expanding a macro)

```clojure
鲮 (expand 'yourcode)
鲮 :m yourcode
```

## プロジェクトの設定 (Configuring a project)

REPL の現在のセッションは「プロジェクト」と呼ばれ、`(Project.config <setting> <value>)` コマンドで設定できます。このコマンドでは、次の項目を設定できます。

- `"cflag"`: コンパイラにフラグを追加します。
- `"libflag"`: コンパイラにライブラリ用のフラグを追加します。
- `"pkgconfigflag"`: pkg-config の呼び出しにフラグを追加します。
- `"compiler"`: `build` コマンドで実行するコンパイラを設定します。
- `"target"`: ターゲットトリプル (target triple) を設定します。クロスコンパイル (cross-compiling) の際に便利です。
- `"title"`: 現在のプロジェクトのタイトルを設定します。生成されるバイナリの名前に影響します。
- `"prompt"`: REPL のプロンプト (prompt) を設定します。
- `"search-path"`: Carp コンパイラが `*.carp` ファイルを探すパスを追加します。
- `"output-directory"`: ビルド成果物の出力先です。
- `"docs-directory"`: 生成されたドキュメントの出力先です。
- `"generate-only"`: ビルド時に C コンパイラを実行したくない場合は、`true` に設定します。

- `"echo-c"`: `def` または `defn` で形式を定義すると、その C コードを表示します。
- `"echo-compiler-cmd"`: プロジェクトのビルド時に、C コンパイラを実行するコマンドを表示します。
- `"print-ast"`: `info` コマンドが、束縛の抽象構文木 (abstract syntax tree、AST) を表示します。

例えば、プロジェクトのタイトルを設定するには、次のようにします。

```clojure
鲮 (Project.config "title" "Fishy")
```

別のコンパイラを使うには、次のようにします。

```clojure
鲮 (Project.config "compiler" "tcc")
```

## プロファイルの設定 (Profile settings)

XDG の設定フォルダー `carp/` に `profile.carp` というファイルを置くと、コンパイラの起動後にそのファイルが読み込まれます。読み込まれるのは、コアライブラリの読み込み後、ほかのソースファイルを読み込む前です。このファイルには、ちょっとした補助関数やその他のカスタマイズなど、すべてのプロジェクトで使いたいユーザー固有の設定を記述します。

> 訳注: 原文の「コアライブラリの読み込み後」という説明は、固定版の実装と一致しません。翻訳元のコミットの [起動処理(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/app/Main.hs#L141-L150) では、`profile.carp` の読み込み、`--eval-preload` の評価、コアライブラリの読み込み、コマンドラインで指定したソースファイルの読み込みの順に処理を呼び出しています。`profile.carp` の読み込みは、ファイルが存在し、プロファイルの読み込みが有効な場合に行われます。

Windows では、このファイルは `C:/Users/USERNAME/AppData/Roaming/carp/profile.carp` にあります。

## コンパイラのフラグ (Compiler flags)

コマンドラインからコンパイラを起動するときは、次のフラグを指定して動作を設定できます。

- `-b`: コードをビルドしてから、コンパイラを終了します。
- `-x`: コードをビルド・実行してから、コンパイラを終了します。`main` 関数が定義されていることを確認してください。
- `--no-core`: コアライブラリを一切読み込まずにコンパイラを実行します。
- `--log-memory`: 実行ファイルが `malloc` と `free` のすべての呼び出しをログに記録します。
- `--optimize`: 配列の境界チェックなどの安全性チェックを取り除き、`-O3` フラグを付けて C コンパイラを実行します。
- `--check`: バイナリを生成せずにコンパイラを実行し、見つかったすべてのエラーだけを機械可読な形式で報告します。
- `--generate-only`: C のソースをコンパイルしません。
- `--eval-preload`: コードを読み込む前に、指定された文字列を評価します。ただし、`profile.carp` の読み込み後です。

## 式から生成された C コードの確認 (Inspecting the C code generated by an expression)

```clojure
鲮 (c '(+ 2 3))
```

## クロスコンパイル (Cross-compiling)

クロスコンパイルは、早い段階で有効にする必要があります。`profile.carp` で次のように設定できます。

```clojure
(Project.config "compiler" "zig cc --target=x86_64-windows-gnu")
(Project.config "target" "x86_64-windows-gnu")
```

または、`--eval-preload` を使って次のように設定できます。

```sh
carp --eval-preload '(Project.config "compiler" "zig cc --target=x86_64-windows-gnu") (Project.config "target" "x86_64-windows-gnu")' -b whatever.carp
```

# 動的評価器 VM (Dynamic Evaluator VM)

原文: [EvaluatorVM.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/EvaluatorVM.md)

翻訳元のコミットは `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` です。
この文書は Carp の開発者・貢献者による英語原文を日本語に翻訳・編集した非公式の文書です。
翻訳方針は [TRANSLATION.md](TRANSLATION.md)、採用語は [GLOSSARY.md](GLOSSARY.md) を参照してください。

Carp の動的評価器 (dynamic evaluator) は、VM を基盤として実装されています。

本書は、アーキテクチャの概要と、今後 VM の開発を行うメンテナー向けのガイドを兼ねています。

## 対象範囲 (Scope)

動的評価器は、次の処理に使われるコンパイル時の実行エンジンです。

1. 動的コード。`defndynamic`、コマンド (commands)、プリミティブ (primitives) が該当します。
2. マクロの展開と実行。
3. `let`、`if`、`while`、`set!`、関数呼び出しなど、評価時に処理する形式。

`src/Eval.hs` は公開 API (`evalDynamic`、`evalStatic`、`eval`) を提供し、実行を VM の処理経路に委ねます。

## 処理の流れ (Pipeline)

評価器の処理の流れは、次のとおりです。

1. `XObj` から `EvalIR` への低水準化 (lowering)。`src/EvalIR.hs` の `lowerExpr` が行います。
2. `EvalIR` から `EvalCode` へのバイトコード (bytecode) コンパイル。`src/EvalVM.hs` の `compileEvalIR` が行います。
3. バイトコードの実行。`src/EvalVM.hs` の `runEvalCode` が行います。

呼び出し可能オブジェクト (callable) のコンパイルには、次の方式があります。

1. 事前にコンパイルする方式 (`VMPrecompiled`)。
2. 初回の呼び出し時にコンパイルし、コンパイル済みコードをキャッシュする方式 (`VMCompileOnCall`)。

## モジュール構成 (Module map)

- `src/Eval.hs`: 評価器の公開エントリーポイント (entrypoint) と、展開処理との統合です。
- `src/EvalIR.hs`: 評価器の中間表現 (IR)、低水準化、復元 (raising、`raiseExpr`) です。
- `src/EvalCode.hs`: バイトコード命令と名前解決ハンドル (resolver handle) の定義です。
- `src/EvalVM.hs`: コンパイルの流れ、名前解決のロジック、ディスパッチ (dispatch)、オペコード (opcode) のループ、キャッシュです。
- `src/EvalVMCore.hs`: 登録された呼び出し可能オブジェクトのコードを実行する、低水準のフレーム (frame)・コードストア (code-store) 処理です。
- `src/EvalSlotLowering.hs`: 局所変数へ高速にアクセスするための、関数内のスロットへの低水準化 (slot lowering) です。
- `src/EvalBound.hs`、`src/EvalBind.hs`: 束縛参照 (bound reference) の表現と補助処理です。
- `src/EvalTypes.hs`: 評価器の名前解決と実行モードに関する型です。

## 実行モードと名前解決の優先設定 (Execution modes and lookup preference)

評価器の動作は、`LookupPreference` で指定するモードによって決まります。

1. `PreferDynamic`
2. `PreferGlobal`
3. `PreferLocal ... ExecFunction|ExecDynamic|ExecMacro`

モードは、名前解決と呼び出し可能オブジェクトのコンパイル方針を制御します。

1. 関数モードでは局所スロット (local slot) が存在することを前提とし、見つからなければ直ちにエラーにします。
2. 動的モードとマクロモードでは、動的な処理に適した名前解決の動作を維持します。

## バイトコードのモデル (Bytecode model)

`EvalCode` は、命令列をリスト形式と配列形式で保持します。主な命令の分類は次のとおりです。

1. スタック・値の操作: `IPushConst`、`IMakeArray`、`IMakeStaticArray`、`IDrop`。
2. 制御フロー: `IJumpIfFalseRel`、`IJumpRel`、`IHalt`、`ITrap`。
3. シンボル・呼び出しのディスパッチ: `IResolveSymbol`、`IExecCallSymbol`、`IExecCall`。
4. 特殊形式の実行操作: `IExecLet`、`IExecFn`、`IExecWhile`、`IExecWith`、`IExecSet`。

`IExecCallSymbol` と `IExecCall` は、実引数の元の IR と、事前にコンパイルした実引数のコードの両方を保持します。そのため、マクロ以外の呼び出しで実引数を評価するときは、ホットパス (hot path) で IR の処理に再帰的に入り直すことを避けられます。

## 呼び出し可能オブジェクトの表現と透過性 (Callable representation and transparency)

VM は、呼び出し可能オブジェクトの実行用データを表すために `VMClosure` を導入していますが、この変更は言語レベルの意味論に対して透過的 (transparent) であるべきです。

現時点で守るべき取り決めは、次のとおりです。

1. 動的関数とマクロの定義は、従来の外側の形式 `(dynamic|macro name params body)` を保ちます。
2. 内部では、実行する本体が VM を基盤とするクロージャ (closure) になっている場合があります。
3. 明示的に変更しない限り、利用者から見えるマクロと動的コードの振る舞いは、VM 導入前の意味論と一致させるべきです。

## キャッシュ (Caching)

関連するキャッシュは、次の 3 つです。

1. 正の `Info.infoIdentifier` をキーとする、IR からバイトコードへの変換のキャッシュ (`evalIRCacheKey`)。
2. `(contextBindingEpoch, symbolId)` をキーとする、オペコードのループ内のシンボル解決キャッシュ。
3. 呼び出しのディスパッチで使う、呼び出し可能オブジェクトの解決キャッシュ。キーには同じ方式を使います。

`contextBindingEpoch` は、環境の状態が変化したときに、キャッシュされた束縛 (binding) を無効化するために使います。

## シンボル解決のモデル (Symbol resolution model)

コンパイル時に、各シンボルに `ResolverHandle` を割り当てます。

1. `RHLocalSlot`
2. `RHGlobal`
3. `RHDynamic`
4. `RHQualified`
5. `RHUnqualified`

オペコードのループでは、まずハンドルの種類に応じて解決し、意味論上必要な場合に限って、より広い範囲の名前解決にフォールバックします。

## スロットへの低水準化の不変条件 (Slot lowering invariants)

関数モードは、スロットへの低水準化に依存します。

1. 関数の仮引数と局所変数への参照は、スロットへの参照に低水準化されます。
2. スロットへの低水準化の後も、局所変数への参照が未解決のまま残っている場合は、エラーとして扱います。
3. `set!` による更新は、局所スロットの状態にも反映され、変更後の読み出しとの整合性を保ちます。

束縛や低水準化の動作を変更する場合は、これらの不変条件 (invariant) を保つか、テストと文書も併せて更新してください。

## VM を安全に変更する方法 (How to make VM changes safely)

評価器の動作を変更するときは、次の手順を踏んでください。

1. 実装だけの変更なのか、言語の意味論を意図的に変更するのかを決めます。
2. 実装だけの変更なら、外側の形式と、外部に見えるエラーの振る舞い (error surface) を保持します。
3. 評価器のテスト (`test/TestEvalIR.hs`、`test/TestEvalSlotLowering.hs`、`test/TestEvalVM.hs`、`test/TestEvalVMCore.hs`) を更新・拡充します。
4. マクロを多用するテストと、動的なクロージャのテスト (`test/macros.carp`、`test/dynamic-closures.carp`) を実行します。
5. ベンチマーク (`./bench/run-evaluator-bench.sh`) を実行し、単発の実行結果ではなく中央値を比較します。

## 性能を調べる手順 (Performance workflow)

主に使うベンチマークスクリプトは、次のものです。

1. `./bench/run-evaluator-bench.sh`

繰り返し実行した結果の中央値を使い、少なくとも次の項目を比較してください。

1. 基準となる起動処理。
2. 評価器のベンチマーク (`bench/evaluator.carp`)。
3. 実際の用途に近いマクロの処理負荷 (`test/macros.carp`)。

## 現時点で目指していないこと (Current non-goal)

評価器 VM (evaluator VM) は、コンパイラ内部の基盤です。利用者のプログラムを実行するための VM ではなく、Carp のコンパイル済みコードの実行モデルを変更するものではありません。

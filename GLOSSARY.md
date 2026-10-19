# 用語集 (Glossary)

翻訳本文・見出し・コードコメントで使用する用語と、文脈による使い分けをまとめています。
原語を併記する語は、各翻訳文書の初出 (コードコメントを含む) で `日本語 (English)` と記載します。
見出しには毎回英語を併記します。表記全般は [翻訳方針](TRANSLATION.md) を参照してください。

## 採用語 (Preferred Terms)

| 英語 | 採用語 | 初出での英語併記・留意点 |
| --- | --- | --- |
| runtime semantics | 実行時の意味論 | 原語を併記します。解釈実行と混同しません |
| dynamic semantics | 動的意味論 | `DynamicSemantics.md` の文書名に使用します。本文では、動的評価器に関する過去の設計目標という位置づけを保持します |
| Static Carp / Dynamic Carp | 静的 Carp / 動的 Carp | `DynamicSemantics.md` が定義する、コンパイルされる版と解釈実行される版の呼称です。初出で原語を併記します |
| sumtype | 直和型 | `直和型 (sumtype)` とします。集合型とは訳しません |
| product type | 直積型 | 原語を併記します。直和型と区別します |
| variant | バリアント | 原語を併記します。型・値・コンストラクタを区別します |
| constructor | コンストラクタ | 型コンストラクタとの区別が必要なら「値コンストラクタ」と明記します |
| type constructor variable | 型コンストラクタ変数 | 原語を併記します |
| named hole | 名前付きホール | 本文で hole を初出併記します |
| hole | ホール | `ホール (hole)` とします |
| binding | 束縛 | 原語を併記します。variable と区別します |
| binding (C library) | バインディング | 原語を併記します。C ライブラリを Carp から利用するための定義を指し、変数の「束縛」と区別します |
| shadowing | シャドーイング | 原語を併記します。同名の別の束縛を隠すことを指します |
| variable | 変数 | — |
| managed type | メモリ管理の対象となる型 | 原語を併記します。GC の存在を意味しません |
| unmanaged | メモリ管理の対象外 | 原語を併記します。参照型かどうかとは別の分類です |
| blittable type | `blit` を実装した型 | 初出で原文の語形を併記します。Carp の `blit` インターフェースとの対応を明示します |
| borrow / borrowing | 借用する / 借用 | 文脈により「貸し出す (借用させる)」と説明できます |
| ownership | 所有権 | give up は「放棄」、take は「取得」とします |
| owning function / ownership-taking function | 所有権を取得する関数 | 初出では原文の語形を併記します。渡された値の所有権を取得することを指します |
| borrowing function | 借用する関数 | 原語を併記します。所有権を取得しないことを指し、値を変更できないという意味には置き換えません |
| generic function | ジェネリック関数 | 原語を併記します。一般的という意味の generic には適用しません |
| generic type | ジェネリック型 | ジェネリック関数と対応させます |
| pattern matching | パターンマッチング | 構文・操作の名称です |
| match group | マッチグループ | 原文との対応を優先します |
| alternation | 選択 | 原語を併記します。記法の説明では「選択記法」も使用できます |
| name lookup | 名前解決 | モジュール内の名前や同名シンボルの解決に使用します |
| qualifier / qualify | 修飾子 / 修飾する | 必要に応じて「モジュール修飾子」とします |
| lens | レンズ | 原語を併記します |
| closure | クロージャ | 原語を併記します |
| getter | getter | 英語で保持します。生成される関数の役割とコードとの対応を優先します |
| setter | setter | 英語で保持します |
| updater | updater | 英語で保持します |
| parameter | 仮引数 | argument との区別が必要な箇所で使用します |
| argument | 実引数 | 区別が不要な一般的説明では「引数」も使用できます |
| static analysis | 静的解析 | — |
| pass (compiler) | パス | 原語を併記します。コンパイラの処理段階を指し、ファイルパスと区別します |
| parsing / parseable | 構文解析 / 構文解析可能な | 初出では原文の語形を併記します。ソースコードを抽象構文へ変換する処理と、その処理が可能であることを表します |
| syntactic analysis | 構文の解析 | 原語を併記します。hacking.md の形式の走査・解析を説明する文脈で使用します |
| abstract data type | 抽象データ型 | 原語を併記します。algebraic data type の「代数的データ型」と取り違えません |
| code emission / emission | コード出力 | 初出では原文の語形を併記します。C コードを出力する段階を指します |
| polymorphism / polymorphic type | 多相性 / 多相型 | 原語を併記し、既存の「多相関数」と対応させます |
| unification | 単一化 | 原語を併記します。型の互換性を調べる文脈で使用します |
| concretization | 具体化 | 原語を併記します。具体的な型への変換を指します |
| constraint / type constraint | 制約 / 型制約 | 原語を併記します。型と型変数の間の制約を扱う文脈で使用します |
| lifetime parameter | ライフタイムパラメーター | 原語を併記し、「ライフタイム」の表記を維持します |
| template | テンプレート | 原語を併記します。C コード生成のための構造を指し、識別子は保持します |
| type candidate | 型の候補 | 原語を併記します。識別子は保持します |
| template generator | テンプレート生成器 | 原語を併記します。テンプレートを生成するものを指します |
| symbol mode | シンボルモード | 原語を併記します。シンボルの扱いを指定するモードを指します |
| scoring | スコアリング | 原語を併記します。型や関数の宣言の並び順を決める文脈で使用します |
| multibranch | 複数の値に対応する分岐 | 原語を併記します。`case` の 1 つの分岐を複数の値に対応させることを指します |
| immutable | 不変 | 原語を併記します。hacking.md では変数の更新を防ぐ目的のメタデータを扱い、その設定だけで更新が禁止されるとは訳しません |
| type inference | 型推論 | 主体の type inferer は「型推論器」です |
| type annotation | 型注釈 | — |
| annotation | 注釈 | 型に限らず、メタデータを付ける文脈では「注釈」とします |
| metadata | メタデータ | 原語を併記します |
| doc string / docstring | ドキュメント文字列 | 初出では原文の語形を併記します |
| dynamic evaluator | 動的評価器 | 原語を併記します。動的コードを評価するものを指します |
| evaluator VM | 評価器 VM | 原語を併記します。VM の表記を保持します |
| bytecode | バイトコード | 原語を併記します。評価器内部で実行する命令を指す文脈で使用します |
| intermediate representation / IR | 中間表現 / IR | 初出は「中間表現 (IR)」とします。識別子 `EvalIR` は保持します |
| callable | 呼び出し可能オブジェクト | 原語を併記します。関数だけに限定せず、呼び出せる対象の総称として使用します |
| raising | 復元 | 原語を併記します。評価器の内部表現を構文表現に戻す文脈で使用します。識別子 `raiseExpr` は保持します |
| resolver handle | 名前解決ハンドル | 原語を併記します。識別子 `ResolverHandle` は保持します |
| dispatch | ディスパッチ | 原語を併記します。呼び出しや命令の処理先を選ぶ文脈で使用します |
| opcode | オペコード | 原語を併記します。個々の命令名は保持します |
| frame | フレーム | 原語を併記します。VM の実行処理におけるフレームを指します |
| code-store | コードストア | 原語を併記します。VM の実行用コードを格納する仕組みを指します |
| slot / local slot | スロット / 局所スロット | 初出で「局所スロット (local slot)」とします。局所変数へのアクセスに使う格納位置を指す文脈で使用します |
| slot lowering | スロットへの低水準化 | 原語を併記します。仮引数や局所変数への参照をスロットへの参照に変換する文脈で使用します |
| bound reference | 束縛参照 | 原語を併記します。名前の束縛を扱う参照表現を指し、すべての名前解決が完了していることは意味しません |
| hot path | ホットパス | 原語を併記します。頻繁に実行される処理経路を指します |
| transparent / transparency | 透過的 / 透過性 | 原語を併記します。内部実装の違いが言語の意味論に影響しないという文脈で使用します |
| invariant | 不変条件 | 原語を併記します。変更時にも維持する必要がある条件を指します |
| error surface | 外部に見えるエラーの振る舞い | 原語を併記します。内部実装だけを変更する際に保持する対象を指します |
| dynamic library | 動的ライブラリ | 原語を併記します。実行ファイルと区別します |
| global variable | グローバル変数 | — |
| child process | 子プロセス | 原語を併記します |
| statically typed | 静的型付け | — |
| reference / reference type | 参照 / 参照型 | 参考情報の reference とは区別します |
| indirection | 間接参照 | `Ref` 型と同一視しません |
| linear pointer type | 線形ポインタ型 | — |
| lifetime | ライフタイム | — |
| linear type / linear type system | 線形型 / 線形型システム | 原語を併記します |
| linear value / non-linear | 線形値 / 非線形 | 原語を併記します。値の種類と型の種類を文脈で区別します |
| owner | 所有者 | 原語を併記します。値に関連付けられたメモリを所有する束縛を指します |
| lexical scope | 字句スコープ | 原語を併記します。ライフタイムと同義にしません |
| dynamic scope | 動的スコープ | 原語を併記します。動的なコードを評価すること自体とは区別します |
| mutable / mutation | 変更可能 / 変更 | 質問文では「変更できますか」と訳せます |
| mutating function | 値を変更する関数 | 原語を併記します。本家の Terminology.md では呼び名と意味を検討中であることを保持します |
| transforming function | 値を変換する関数 | 原語を併記します。本家の Terminology.md の見出しの訳です。endo-functions は英語で保持し、命名が検討中であることを保持します |
| unsafe function | 安全でない関数 | 原語を併記します。`unsafe-` は任意の命名規則であることを保持します |
| functional | 関数型の | プログラミング言語の性質を表す語です。`function type` が指す型とは区別します |
| GC / GC'ed | GC / GC によるメモリ管理を行う | GC の英語表記を保持します。動的 Carp の説明と、コンパイルされる Carp のメモリ管理を混同しません |
| move / moving | ムーブ | 初出では原文の語形を併記します。所有権の移譲を表す操作に使用します |
| transfer of ownership | 所有権の移譲 | 原語を併記します。take / give up の「取得 / 放棄」とは文法に応じて使い分けます |
| copy / copying | コピー | 操作名として使用します。copying が概念の初出なら原語を併記します |
| use after free / double free | 解放後の使用 / 二重解放 | 原語を併記します |
| memory allocation | メモリの割り当て | deallocation の「解放」と対になる操作です |
| deterministic memory management | 決定論的なメモリ管理 | 原語を併記します。日常語の「決定的」と区別しやすい表記として、この文脈では「決定論的」を使用します |
| ownership tracking | 所有権の追跡 | 原語を併記します。所有権の取得・放棄とは区別します |
| sound synthesis | 音響合成 | 原語を併記します。音声に限定せず、音を合成する文脈で使用します |
| abstract syntax tree / AST | 抽象構文木 / AST | 初出は「抽象構文木 (abstract syntax tree、AST)」とします |
| deleter | deleter | 英語で保持します。Memory.md の実装説明では削除処理の情報を保持するデータ構造を指し、削除関数そのものとは区別します |
| deletion function / deletion routine | 削除関数 / 削除処理 | メモリの解放を述べる場合は「解放」と訳し、値の削除と動作を区別します |
| liveness analysis | 生存性解析 | 原語を併記します |
| dangling reference | ダングリング参照 | 原語を併記します |
| source variable | 参照元の変数 | 原語を併記します。Memory.md の参照の依存関係を扱う文脈で使用します |
| live set | 生存集合 | 原語を併記します |
| lifetime mode / lifetime map | ライフタイムモード / ライフタイムマップ | 原語を併記します。個々の mapping は「対応付け」とします |
| borrow checker | 借用チェッカー | 原語を併記します。Carp と Rust のどちらの説明かを文脈で区別します |
| borrow checking | 借用チェック | 原語を併記します。借用に関する検査処理を指し、検査する主体の「借用チェッカー」と区別します |
| generic programming | ジェネリックプログラミング | 原語を併記し、既存のジェネリック関数・ジェネリック型と対応させます |
| polymorphic function | 多相関数 | 原語を併記します |
| memory state | メモリ状態 | 原語を併記します。識別子 `MemState` は変更しません |
| deallocation | 解放 | 「開放」にしません |
| primitive | プリミティブ型 | primitive constants は「プリミティブ型の定数」とします |
| data literal / type literal | データリテラル / 型リテラル | — |
| type variable | 型変数 | — |
| function type | 関数型 | `Fn` は識別子として保持します |
| dynamic code / dynamic function | 動的コード / 動的関数 | 動的型付けと同義にしません |
| macro / reader macro | マクロ / リーダーマクロ | — |
| hygienic | 衛生的 | 原語を併記します。マクロの性質を表す用語です |
| quote / quasiquotation / quasiquoting | クォート / 準クォート | 準クォートは初出で原文の語形を併記します。識別子 `quote`、`quasiquote` は保持します |
| unquote / unquoting / unquoted | アンクォート | 初出では原文の語形を併記します。クォートを解除して対象の式を評価することを指します。識別子 `unquote` は保持します |
| splicing | スプライシング | 原語を併記します。リストの要素を入れ子にせずに差し込む操作を指します。識別子 `unquote-splicing` は保持します |
| macro expansion | マクロ展開 | — |
| rest arguments | 残余引数 | 原語を併記します。残りの実引数をまとめて受け取るものを指します |
| variadic | 可変長引数の | 残余引数の仕組みそのものとは区別します |
| dynamic environment | 動的環境 | 原語を併記します。動的コードで使用する環境を指します |
| primitive (evaluator form) | プリミティブ | 原語を併記します。評価器が扱う形式の分類を指し、プリミティブ型とは区別します。識別子 `Primitive` は保持します |
| command (evaluator form) | コマンド | 原語を併記します。評価器が扱う形式の分類を指す場合に使用します |
| lowering | 低水準化 | 原語を併記します。評価器の内部表現への変換を指す文脈で使用します |
| context | コンテキスト | 原語を併記します。コンパイラの状態や、動的・静的などのコードを評価する文脈を指します。識別子 `Context` は保持します |
| evaluation frame | 評価フレーム | 原語を併記します |
| traceback | トレースバック | 原語を併記します。エラーに付随する評価の履歴を指します |
| stack trace | スタックトレース | 原語を併記します。原文の traceback との語の違いを保持します |
| reserved name | 予約名 | 初出では原文の語形を併記します。キーワードという別の分類と同一視しません |
| namespace | 名前空間 | 原語を併記します。スコープと区別します |
| reflection | リフレクション | 初出では原文の語形を併記します |
| first-class citizen / first class citizens | 第一級オブジェクト | 初出では原文の語形を併記します |
| higher order function | 高階関数 | 初出では原文の語形を併記します |
| special form / form | 特殊形式 / 形式 | form をすべて特殊形式と訳しません |
| REPL | REPL | 大文字の英語表記を保持します |
| prompt | プロンプト | 原語を併記します。REPL などで、入力を待っていることを示す表示を指します |
| search path | 検索パス | Carp の設定名 `search-path` はそのまま保持します |
| library / standard library / external library | ライブラリ / 標準ライブラリ / 外部ライブラリ | モジュールとは区別します。Core の固有名は保持します |
| entrypoint | エントリーポイント | 原語を併記します。ライブラリを読み込む際の入口となるファイルや、処理を呼び出す入口となる関数を指す文脈で使用します |
| wrapper | ラッパー | 原語を併記します |
| port (of a library) | 移植版 | 移植したライブラリを指す場合に使用します。通信のポートとは区別します |
| terminal | ターミナル | REPL やシェルそのものとは区別します |
| top-level | トップレベル | top-level expression は「トップレベルの式」とします |
| mutual recursion | 相互再帰 | — |
| tail position | 末尾位置 | — |
| self-recursive | 自己再帰 | — |
| stack overflow | スタックオーバーフロー | — |
| side effect | 副作用 | — |
| identity function | 恒等関数 | — |
| struct / structure type | 構造体 / 構造体型 | — |
| enumeration | 列挙型 | — |
| recursive type | 再帰型 | — |
| module / symbol / scope | モジュール / シンボル / スコープ | local は「局所」を基本とします |
| interface / implementation | インターフェース / 実装 | 識別子は翻訳しません |
| derivation / automatic derivation | 導出 / 自動導出 | 原語を併記します。API 名の `derive` は保持します |
| deriver | 導出器 | 原語を併記します。型からインターフェースの実装を生成するルールを指します |
| concrete (type) | 具体的な型 | 原文の形容詞 concrete を初出で併記します。Derive.md では、型変数を含まない型という定義を保持します |
| unary interface | 単項インターフェース | 原語を併記します。引数を 1 つ受け取るインターフェースを指します |
| boilerplate | 定型コード | 原語を併記します。実装本体を囲む定型的なコードを指す文脈で使用します |
| type signature | 型シグネチャ | 単に「シグネチャ」と短縮せず統一します |
| ambiguity | 曖昧性 | 「曖昧さ」の方が文脈上自然な場合はその表現も使用できます |
| C interop | C との相互運用 | — |
| opaque type | 不透明な型 | C の型なら「不透明な C 型」とします |
| emitted C code | 生成される C コード | — |
| mangling | 名前マングリング | 原語を併記します。C 向けに識別子を変換する処理を指し、モジュールの「修飾子」と区別します |
| allocator | アロケータ | 原語を併記します。メモリの割り当てに使用するものを指します |
| initializer | 初期化関数 | 原語を併記します。CInterop.md では、型の値を構築する関数を指します |
| callback | コールバック | — |
| lambda | ラムダ | 原語を併記します。既存の「ラムダ関数」も使用できます |
| capture | キャプチャする | ラムダが環境の変数を取り込む文脈で使用します |
| coerce | 強制変換する | 参照やポインタの型を変換する文脈で使用します。型安全性を保証する表現にしません |
| static function | 静的関数 | Carp の関数を分類する文脈で使用します。C の `static` 指定とは同一視しません |
| preprocessor directive | プリプロセッサディレクティブ | 原語を併記します |
| generics | ジェネリクス | ジェネリックな型や関数を扱う仕組みの総称です |
| kebab-case | ケバブケース | 原語を併記します。ハイフンで単語を区切る識別子の表記です |
| executable | 実行ファイル | ビルドの成果物や、実行するファイルを指す場合に使用します |
| build artifact | ビルド成果物 | ビルドによって生成されたものを指します |
| target triple | ターゲットトリプル | 原語を併記します |
| cross-compilation / cross-compiling | クロスコンパイル | 初出では原文の語形を併記します |
| cross-compiler | クロスコンパイラ | 原語を併記します。クロスコンパイルを行うコンパイラを指します |
| embedded device / embedded system | 組み込み機器 / 組み込みシステム | 初出では原文の語形を併記します。組み込み関数を指す built-in と区別します |
| host system | ホストシステム | 原語を併記します。ビルドを行う環境を指し、実行対象と区別します |
| target platform | ターゲットプラットフォーム | 原語を併記します。実行対象の環境を指します |
| linker script | リンカースクリプト | 原語を併記します。リンカーに渡すスクリプトを指します |
| prelude | プレリュード | 原語を併記します。Embedded.md では、標準定義を読み込む core/Core.carp を指します |
| Link Time Optimization / LTO | リンク時最適化 / LTO | 初出は「リンク時最適化 (Link Time Optimization、LTO)」とします |
| cache miss | キャッシュミス | 原語を併記します |
| static array | 静的配列 | 原語を併記します。リテラル `$[]` と識別子 `StaticArray` は保持します |
| binary | バイナリ | 実行ファイルを指す場合も、原文の executable との語の違いを保持します |
| environment variable | 環境変数 | 変数名や設定コマンドは変更しません |
| locale | ロケール | 原語を併記します。local の「局所」と区別します |
| linker | リンカー | コンパイルとリンクを区別します |
| include path | インクルードパス | ヘッダーファイルなどを探すためのパスを指します |
| linking flag | リンクフラグ | リンク時に指定するオプションを指します |
| rendering context | レンダリングコンテキスト | 原語を併記します。一般的な「文脈」と訳しません |
| encoding | 文字エンコーディング | ファイルの文字の符号化方式を指す場合に使用します |
| syntax highlighting / highlight | 構文ハイライト | 初出では原文の語形を併記します。「シンタックスハイライト」と混在させません |
| grammar (editor support) | 文法定義 | 原語を併記します。エディターの言語サポートで、構文を記述する定義を指す文脈で使用します |
| editor mode | エディターモード | 原語を併記します。特定のエディターだけに限定せず、原文の言語サポートの呼称を保持します |
| format string | 書式指定文字列 | 原語を併記します。「フォーマット文字列」と混在させません |
| format specifier | 書式指定子 | 原語を併記します。書式指定文字列全体と区別します |
| directive (format string) | 変換指定 | 原語を併記します。書式指定文字列中で値の変換を指定する部分です。preprocessor directive と区別します |
| pattern / regular expression | パターン / 正規表現 | 同一視しません |
| programming pattern | プログラミングパターン | 原語を併記します。プログラムの書き方を指し、パターンマッチングや文字列のパターンと区別します |
| backtrack | バックトラック | 原文の主張の範囲を独自に拡大しません |
| non-greedy | 非貪欲 | — |
| list / array | リスト / 配列 | `list` 関数や `Array` 型の名前は保持します |

## 文脈による訳し分け (Contextual Usage)

- reference は、型・値の「参照」、名前を「参照する」操作、参考資料という意味の「参考」を区別します。
- generic は、技術概念の「ジェネリック」と、一般的な分岐などを指す「一般的」を区別します。
- match は、操作の「パターンマッチング」、文字列の結果の「一致」、識別子としての API 名を区別します。
- managed と reference は別の軸です。メモリ管理の対象であることから参照型であると推論しません。
- binding は、名前と値を関連付ける「束縛」と、C ライブラリを利用するための「バインディング」を区別します。

## 選定の参考 (Terminology Reference)

日本語表記の参考資料です。

- [Rust By Example: クロージャ](https://doc.rust-lang.org/rust-by-example/ja/fn/closures.html)
- [Rust By Example: 所有権とムーブ](https://doc.rust-lang.org/rust-by-example/ja/scope/move.html)
- [Rust By Example: 導出](https://doc.rust-jp.rs/rust-by-example-ja/trait/derive.html)
- [Gauche ユーザリファレンス: 衛生的マクロ](https://practical-scheme.net/gauche/man/gauche-refj/Wei-Sheng-De-makuro.html)
- [Gauche ユーザリファレンス: 準クオート](https://practical-scheme.net/gauche/man/gauche-refj/Zhun-kuoto.html)
- [Gauche ユーザリファレンス: 手続きを作る](https://practical-scheme.net/gauche/man/gauche-refj/Shou-Sok-kiwoZuo-ru.html)
- [Python 言語リファレンス: 呼び出し](https://docs.python.org/ja/3/reference/expressions.html#calls)
- [筑波大学 ソフトウェア技法: 直積型と代数的データ型](https://www.logic.cs.tsukuba.ac.jp/~kam/lecture/fp2016/6.pdf)
- [MDN: 関数](https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Functions)
- [Microsoft Learn: 書式指定構文](https://learn.microsoft.com/ja-jp/cpp/c-runtime-library/format-specification-syntax-printf-and-wprintf-functions?view=msvc-170)

# 用語集 (Glossary)

翻訳本文・見出し・コードコメントで使用する用語と、文脈による使い分けをまとめています。
原語を併記する語は、各翻訳文書の初出 (コードコメントを含む) で `日本語 (English)` と記載します。
見出しには毎回英語を併記します。表記全般は [翻訳方針](TRANSLATION.md) を参照してください。

## 採用語 (Preferred Terms)

| 英語 | 採用語 | 初出での英語併記・留意点 |
| --- | --- | --- |
| runtime semantics | 実行時の意味論 | 原語を併記します。解釈実行と混同しません |
| sumtype | 直和型 | `直和型 (sumtype)` とします。集合型とは訳しません |
| variant | バリアント | 原語を併記します。型・値・コンストラクタを区別します |
| constructor | コンストラクタ | 型コンストラクタとの区別が必要なら「値コンストラクタ」と明記します |
| type constructor variable | 型コンストラクタ変数 | 原語を併記します |
| named hole | 名前付きホール | 本文で hole を初出併記します |
| hole | ホール | `ホール (hole)` とします |
| binding | 束縛 | 原語を併記します。variable と区別します |
| binding (C library) | バインディング | 原語を併記します。C ライブラリを Carp から利用するための定義を指し、変数の「束縛」と区別します |
| variable | 変数 | — |
| managed type | メモリ管理の対象となる型 | 原語を併記します。GC の存在を意味しません |
| unmanaged | メモリ管理の対象外 | 原語を併記します。参照型かどうかとは別の分類です |
| borrow / borrowing | 借用する / 借用 | 文脈により「貸し出す (借用させる)」と説明できます |
| ownership | 所有権 | give up は「放棄」、take は「取得」とします |
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
| type inference | 型推論 | 主体の type inferer は「型推論器」です |
| type annotation | 型注釈 | — |
| statically typed | 静的型付け | — |
| reference / reference type | 参照 / 参照型 | 参考情報の reference とは区別します |
| indirection | 間接参照 | `Ref` 型と同一視しません |
| linear pointer type | 線形ポインタ型 | — |
| lifetime | ライフタイム | — |
| linear type / linear type system | 線形型 / 線形型システム | 原語を併記します |
| linear value / non-linear | 線形値 / 非線形 | 原語を併記します。値の種類と型の種類を文脈で区別します |
| owner | 所有者 | 原語を併記します。値に関連付けられたメモリを所有する束縛を指します |
| lexical scope | 字句スコープ | 原語を併記します。ライフタイムと同義にしません |
| move / moving | ムーブ | 初出では原文の語形を併記します。所有権の移譲を表す操作に使用します |
| transfer of ownership | 所有権の移譲 | 原語を併記します。take / give up の「取得 / 放棄」とは文法に応じて使い分けます |
| copy / copying | コピー | 操作名として使用します。copying が概念の初出なら原語を併記します |
| use after free / double free | 解放後の使用 / 二重解放 | 原語を併記します |
| memory allocation | メモリの割り当て | deallocation の「解放」と対になる操作です |
| abstract syntax tree / AST | 抽象構文木 / AST | 初出は「抽象構文木 (abstract syntax tree、AST)」とします |
| deleter | deleter | 英語で保持します。Memory.md の実装説明では削除処理の情報を保持するデータ構造を指し、削除関数そのものとは区別します |
| deletion function / deletion routine | 削除関数 / 削除処理 | メモリの解放を述べる場合は「解放」と訳し、値の削除と動作を区別します |
| liveness analysis | 生存性解析 | 原語を併記します |
| dangling reference | ダングリング参照 | 原語を併記します |
| source variable | 参照元の変数 | 原語を併記します。Memory.md の参照の依存関係を扱う文脈で使用します |
| live set | 生存集合 | 原語を併記します |
| lifetime mode / lifetime map | ライフタイムモード / ライフタイムマップ | 原語を併記します。個々の mapping は「対応付け」とします |
| borrow checker | 借用チェッカー | 原語を併記します。原文が Rust の用語として示す文脈を保持します |
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
| special form / form | 特殊形式 / 形式 | form をすべて特殊形式と訳しません |
| REPL | REPL | 大文字の英語表記を保持します |
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
| pattern / regular expression | パターン / 正規表現 | 同一視しません |
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

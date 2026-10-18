# 用語集 (Glossary)

この表の「採用語」を翻訳本文・見出し・コードコメントで使用します。
原語を併記する語は、各翻訳文書の本文初出のみ `日本語 (English)` とします。見出しの英語併記は別の規則です。
本表には英語欄があるため、日本語欄では原語を重複して記しません。

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
| variable | 変数 | 現行語を保持します |
| managed type | メモリ管理の対象となる型 | 原語を併記します。GC の存在を意味しません |
| unmanaged | メモリ管理の対象外 | 原語を併記します。参照型かどうかとは別の分類です |
| borrow / borrowing | 借用する / 借用 | 文脈により「貸し出す (借用させる)」と説明できます |
| ownership | 所有権 | give up は「放棄」、take は「取得」とします |
| generic function | ジェネリック関数 | 原語を併記します。一般的という意味の generic には適用しません |
| generic type | ジェネリック型 | ジェネリック関数と対応させます |
| pattern matching | パターンマッチング | 構文・操作の名称です |
| match group | マッチグループ | 原文との対応を優先します |
| alternation | 選択 | 原語を併記します。記法の説明では「選択記法」も使用できます |
| name lookup | 名前解決 | 原文の節は名前の曖昧性の解消も扱うため、この語を採用します |
| qualifier / qualify | 修飾子 / 修飾する | 必要に応じて「モジュール修飾子」とします |
| lens | レンズ | `レンズ (lens)` とします。概念名を日本語表記で追えるようにする採択です |
| closure | クロージャ | `クロージャ (closure)` とします。日本語のプログラミング文書で使われる概念名を採用します |
| getter | getter | 英語で保持します。生成される関数の役割とコードとの対応を優先します |
| setter | setter | 英語で保持します |
| updater | updater | 英語で保持します |
| parameter | 仮引数 | argument との区別が必要な箇所で使用します |
| argument | 実引数 | 区別が不要な一般的説明では「引数」も使用できます |
| static analysis | 静的解析 | 現行語を保持します |
| type inference | 型推論 | 主体の type inferer は「型推論器」です |
| type annotation | 型注釈 | 現行語を保持します |
| statically typed | 静的型付け | 現行語を保持します |
| reference / reference type | 参照 / 参照型 | 参考情報の reference とは区別します |
| indirection | 間接参照 | `Ref` 型と同一視しません |
| linear pointer type | 線形ポインタ型 | 現行語を保持します |
| lifetime | ライフタイム | 「生存期間」へ置換しません |
| deallocation | 解放 | 「開放」にしません |
| primitive | プリミティブ型 | constants などの限定を省略しません |
| data literal / type literal | データリテラル / 型リテラル | 現行語を保持します |
| type variable | 型変数 | 英語のまま残しません |
| function type | 関数型 | `Fn` は識別子として保持します |
| dynamic code / dynamic function | 動的コード / 動的関数 | 動的型付けと同義にしません |
| macro / reader macro | マクロ / リーダーマクロ | 現行語を保持します |
| special form / form | 特殊形式 / 形式 | form をすべて特殊形式と訳しません |
| REPL | REPL | 大文字の英語表記を保持します |
| mutual recursion | 相互再帰 | 現行語を保持します |
| tail position | 末尾位置 | 現行語を保持します |
| self-recursive | 自己再帰 | 現行語を保持します |
| stack overflow | スタックオーバーフロー | 現行語を保持します |
| side effect | 副作用 | 現行語を保持します |
| identity function | 恒等関数 | 現行語を保持します |
| struct / structure type | 構造体 / 構造体型 | 現行語を保持します |
| enumeration | 列挙型 | 現行語を保持します |
| recursive type | 再帰型 | 現行語を保持します |
| module / symbol / scope | モジュール / シンボル / スコープ | 現行語を保持します。local は「局所」を基本とします |
| interface / implementation | インターフェース / 実装 | 識別子は翻訳しません |
| type signature | 型シグネチャ | 単に「シグネチャ」と短縮せず統一します |
| ambiguity | 曖昧性 | 「曖昧さ」の方が文脈上自然な場合はその表現も使用できます |
| C interop | C との相互運用 | 現行語を保持します |
| opaque type | 不透明な型 | C の型なら「不透明な C 型」とします |
| emitted C code | 生成される C コード | 現行語を保持します |
| pattern / regular expression | パターン / 正規表現 | 同一視しません |
| backtrack | バックトラック | 原文の主張の範囲を独自に拡大しません |
| non-greedy | 非貪欲 | 現行語を保持します |
| list / array | リスト / 配列 | `list` 関数や `Array` 型の名前は保持します |

## 文脈による訳し分け (Contextual Usage)

- reference は、型・値の「参照」、名前を「参照する」操作、参考資料という意味の「参考」を区別します。
- generic は、技術概念の「ジェネリック」と、一般的な分岐などを指す「一般的」を区別します。
- match は、操作の「パターンマッチング」、文字列の結果の「一致」、識別子としての API 名を区別します。
- managed と reference は別の軸です。メモリ管理の対象であることから参照型であると推論しません。
- getter、setter、updater の英語保持は本プロジェクトの表記選択です。カタカナ表記を一般に誤りとする規則ではありません。
- レンズの日本語表記も本プロジェクトの選択です。識別子やライブラリ名までカタカナにしません。

## 選定の参考 (Terminology Reference)

クロージャは [Rust By Example の日本語版](https://doc.rust-lang.org/rust-by-example/ja/fn/closures.html) でも使用されている表記です。
この資料は日本語表記の参考であり、Carp の仕様を Rust の仕様で補うためには使用しません。

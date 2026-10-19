# 変更履歴 (Changelog)

原文: [CHANGELOG.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/CHANGELOG.md)

翻訳元のコミットは `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` です。
この文書は Carp の開発者・貢献者による英語原文を日本語に翻訳・編集した非公式の文書です。
翻訳方針は [TRANSLATION.md](TRANSLATION.md)、採用語は [GLOSSARY.md](GLOSSARY.md) を参照してください。

> 訳注: 原文の収録範囲は 0.5.1〜0.5.5 です。固定版の [Carp の紹介](Carp-JP.md) で案内されている 0.6.0 の項目は、原文に収録されていません。この文書は、固定コミットまでのすべての変更を網羅したものではありません。

## 0.5.5

- docs: Markdown 文書の見出しレベル 1 (`h1`) を 1 つだけに統一しました ([#1418(英語)](https://github.com/carp-lang/Carp/issues/1418))。
- feat: `IO` に `fputc` のラッパー (wrapper) を追加しました ([#1417(英語)](https://github.com/carp-lang/Carp/issues/1417))。
- feat: `stdint` の型に対して `MAX` と `MIN` のマクロを登録しました ([#1412(英語)](https://github.com/carp-lang/Carp/issues/1412))。
- fix: インターフェースの具体化 (concretization) で、シンボルモード (symbol modes) を正しく扱うようにしました ([#1415(英語)](https://github.com/carp-lang/Carp/issues/1415))。
- fix: メモリ管理で、`let` の束縛 (binding) のシャドーイング (shadowing) を正しく扱うようにしました ([#1413(英語)](https://github.com/carp-lang/Carp/issues/1413))。
- feat: `Dynamic.sort` を追加し、失敗した動的テストの出力を改善しました ([#1411(英語)](https://github.com/carp-lang/Carp/issues/1411))。
- feat: `ByteOrder` に `blit` を実装しました ([#1410(英語)](https://github.com/carp-lang/Carp/issues/1410))。
- chore: Stackage のバージョンを 19.2 に更新しました ([#1408(英語)](https://github.com/carp-lang/Carp/issues/1408))。
- feat: `blit` を実装した型 (blittable types) を、メモリ管理の対象外にしました ([#1407(英語)](https://github.com/carp-lang/Carp/issues/1407))。
- ci: Windows で `Debug.sanitize` を再び有効にしました ([#1406(英語)](https://github.com/carp-lang/Carp/issues/1406))。
- feat: `IO.fgetc` を追加しました ([#1405(英語)](https://github.com/carp-lang/Carp/issues/1405))。
- feat: 配列で `cons-last` を使えるようにしました ([#1402(英語)](https://github.com/carp-lang/Carp/issues/1402))。
- refactor: プロジェクト設定の取得と設定で扱える項目をそろえました ([#1400(英語)](https://github.com/carp-lang/Carp/issues/1400))。
- ci: Scoop を管理者ユーザーとしてインストールする処理を修正しました ([#1399(英語)](https://github.com/carp-lang/Carp/issues/1399))。
- feat: `c-name` メタフィールドを追加しました ([#1398(英語)](https://github.com/carp-lang/Carp/issues/1398))。
- feat: `Dynamic.String.to-array` を追加しました ([#1382(英語)](https://github.com/carp-lang/Carp/issues/1382))。
- fix: setter のテンプレート (template) で、フィールド名の名前マングリング (mangling) を修正しました ([#1379(英語)](https://github.com/carp-lang/Carp/issues/1379))。
- fix: `fmt` の先頭の `%` の扱いを修正しました ([#1380(英語)](https://github.com/carp-lang/Carp/issues/1380))。
- fix: C コードの表示時にジェネリック型のシンボルを無視することで、[#1347(英語)](https://github.com/carp-lang/Carp/issues/1347) を修正しました ([#1373(英語)](https://github.com/carp-lang/Carp/issues/1373))。
- fix: 正しい設定キー `pkg-configDepends` を使用して、Nix でのインストールを修正しました ([#1372(英語)](https://github.com/carp-lang/Carp/issues/1372))。
- fix: `Array.unsafe-raw` の型シグネチャを修正しました ([#1375(英語)](https://github.com/carp-lang/Carp/issues/1375))。
- docs: UTF-8 を正しく扱うための手順を追加しました ([#1367(英語)](https://github.com/carp-lang/Carp/issues/1367))。

## 0.5.4

- refactor: 型の候補 (type candidates) とテンプレート生成器 (template generators) を追加しました ([#1361(英語)](https://github.com/carp-lang/Carp/issues/1361))。
- fix: フィールドを持つ登録型でパスが出力されるようにしました ([#1364(英語)](https://github.com/carp-lang/Carp/issues/1364))。
- fix: モジュール内で型を登録できるようにしました ([#1362(英語)](https://github.com/carp-lang/Carp/issues/1362))。
- feat: `Box` 型を追加しました ([#1358(英語)](https://github.com/carp-lang/Carp/issues/1358))。
- feat: `bytes->hex-string` を追加しました ([#1354(英語)](https://github.com/carp-lang/Carp/issues/1354))。
- feat: `headerparse` で C の識別子を常に出力するフラグを追加しました ([#1353(英語)](https://github.com/carp-lang/Carp/issues/1353))。
- docs: コアの式にドキュメントを追加しました ([#1350(英語)](https://github.com/carp-lang/Carp/issues/1350)) ([#1352(英語)](https://github.com/carp-lang/Carp/issues/1352))。
- test: `match` で所有権を放棄した値を使用するエラーのテストを追加しました ([#1351(英語)](https://github.com/carp-lang/Carp/issues/1351))。
- fix: Unit 型を指定した `the` で、不要な変数への代入を出力しないようにしました ([#1349(英語)](https://github.com/carp-lang/Carp/issues/1349))。
- fix: [#1064(英語)](https://github.com/carp-lang/Carp/issues/1064) と [#843(英語)](https://github.com/carp-lang/Carp/issues/843) のバグを修正しました ([#1321(英語)](https://github.com/carp-lang/Carp/issues/1321))。
- fix: モジュールの展開時に処理が進まなくなる問題を修正しました ([#1340(英語)](https://github.com/carp-lang/Carp/issues/1340))。
- feat: `scan` 関数群を追加しました ([#1339(英語)](https://github.com/carp-lang/Carp/issues/1339))。
- fix: オブジェクトが実際には `Mod` である場合に、`If` を `InvalidObj` に渡さないようにしました ([#1327(英語)](https://github.com/carp-lang/Carp/issues/1327))。
- feat: `register-type` を改善しました ([#1332(英語)](https://github.com/carp-lang/Carp/issues/1332))。
- fix: `ControlMacros.carp` を更新しました ([#1336(英語)](https://github.com/carp-lang/Carp/issues/1336))。
- fix: 静的な呼び出しを正しく分類するようにしました ([#1322(英語)](https://github.com/carp-lang/Carp/issues/1322))。
- docs: `Macros.md` の誤記を修正しました ([#1331(英語)](https://github.com/carp-lang/Carp/issues/1331))。
- docs: `Install.md` を更新しました ([#1324(英語)](https://github.com/carp-lang/Carp/issues/1324))。
- feat: 代入演算子のマクロを追加しました ([#1320(英語)](https://github.com/carp-lang/Carp/issues/1320))。
- feat: 直和型 (sumtype) のコンストラクタ数の上限に関するコンパイルエラーを追加しました ([#1319(英語)](https://github.com/carp-lang/Carp/issues/1319))。

## 0.5.3

- ci: プラットフォームごとに分かれていたリリースを 1 つにまとめました ([#1313(英語)](https://github.com/carp-lang/Carp/issues/1313))。
- feat: `Dynamic.List.find-index` を追加しました ([#1316(英語)](https://github.com/carp-lang/Carp/issues/1316))。
- feat: `expand-compiled` を追加しました ([#1310(英語)](https://github.com/carp-lang/Carp/issues/1310))。
- fix: Windows で、非推奨ではない `unlink` 関数を使うようにしました ([#1311(英語)](https://github.com/carp-lang/Carp/issues/1311))。

## 0.5.2

- fix: `void` の定義を省略するようにしました ([#1305(英語)](https://github.com/carp-lang/Carp/issues/1305))。
- fix: モジュール内で定義した型をメンバーに使えるようにしました ([#1303(英語)](https://github.com/carp-lang/Carp/issues/1303))。
- fix: インターフェースの値が破棄されないようにしました ([#1308(英語)](https://github.com/carp-lang/Carp/issues/1308))。
- feat: `Float.round` を追加しました ([#1301(英語)](https://github.com/carp-lang/Carp/issues/1301))。
- feat: `ignore` 系のマクロを追加しました ([#1300(英語)](https://github.com/carp-lang/Carp/issues/1300))。
- fix: 入れ子になった多相型 (polymorphic types) を修正しました ([#1294(英語)](https://github.com/carp-lang/Carp/issues/1294))。
- refactor: `Concretize` モジュールを整理しました ([#1283(英語)](https://github.com/carp-lang/Carp/issues/1283))。
- fix: 型と関数の宣言のスコアリング (scoring) を修正しました ([#1290(英語)](https://github.com/carp-lang/Carp/issues/1290))。
- fix: `String.prn` で引用符をエスケープするようにしました ([#1287(英語)](https://github.com/carp-lang/Carp/issues/1287))。
- fix: 修飾されたシンボルに対して `Symbol.prefix` が動作するようにしました ([#1286(英語)](https://github.com/carp-lang/Carp/issues/1286))。
- fix: REPL で行番号を正しく扱うようにしました ([#1282(英語)](https://github.com/carp-lang/Carp/issues/1282))。
- fix: 動的な `let` の束縛における再帰と、binder のリークを修正しました ([#1281(英語)](https://github.com/carp-lang/Carp/issues/1281))。
- feat: `Dynamic.Debug.trace` を追加しました ([#1279(英語)](https://github.com/carp-lang/Carp/issues/1279))。
- feat: `Dynamic.proc?` を追加しました ([#1278(英語)](https://github.com/carp-lang/Carp/issues/1278))。
- feat: `List.remove-nth` を追加しました ([#1277(英語)](https://github.com/carp-lang/Carp/issues/1277))。
- feat: `machine-info` プリミティブ (primitive) の試案を追加しました ([#1269(英語)](https://github.com/carp-lang/Carp/issues/1269))。
- feat: `case` で複数の値に対応する分岐 (multibranches) を扱えるようにしました ([#1276(英語)](https://github.com/carp-lang/Carp/issues/1276))。
- docs: プリミティブとコマンド (commands) に `infoFile` を設定しました ([#1273(英語)](https://github.com/carp-lang/Carp/issues/1273))。
- docs: コアモジュールのドキュメントを追加しました ([#1271(英語)](https://github.com/carp-lang/Carp/issues/1271))。
- fix: `defmodule` に正しい情報を設定しました ([#1270(英語)](https://github.com/carp-lang/Carp/issues/1270))。
- docs: パターンの制限を文書化しました ([#1268(英語)](https://github.com/carp-lang/Carp/issues/1268))。
- fix: Windows の 32 ビット版 TCC で Carp を使えるよう、不足していた定義を追加しました ([#1267(英語)](https://github.com/carp-lang/Carp/issues/1267))。
- docs: トップレベルで `doc` が動作するようにし、マクロを文書化しました ([#1265(英語)](https://github.com/carp-lang/Carp/issues/1265))。
- feat: トップレベルの束縛のドキュメントを出力するようにしました ([#1253(英語)](https://github.com/carp-lang/Carp/issues/1253))。
- fix: `Dynamic.String.slice` の添字の扱いを修正しました ([#1258(英語)](https://github.com/carp-lang/Carp/issues/1258))。
- feat: `(and)` と `(or)` が任意の個数の引数を扱えるようにしました ([#1251(英語)](https://github.com/carp-lang/Carp/issues/1251))。
- feat: `IO.Raw` を追加しました ([#1243(英語)](https://github.com/carp-lang/Carp/issues/1243))。
- fix: ビルド時にジェネリックな `main` を検査するようにしました ([#1247(英語)](https://github.com/carp-lang/Carp/issues/1247))。
- docs: メモリ管理の文書を更新し、`delete` の上書きを推奨しないことを明記しました ([#1245(英語)](https://github.com/carp-lang/Carp/issues/1245))。
- docs: `managed?` プリミティブを文書化しました ([#1244(英語)](https://github.com/carp-lang/Carp/issues/1244))。
- fix: HTML ドキュメントにサブモジュールを表示するようにしました ([#1242(英語)](https://github.com/carp-lang/Carp/issues/1242))。
- fix: REPL での関数適用の評価を修正しました ([#1238(英語)](https://github.com/carp-lang/Carp/issues/1238))。
- refactor: 形式の検証処理を別のモジュールに移しました ([#1233(英語)](https://github.com/carp-lang/Carp/issues/1233))。

## 0.5.1

- fix: 構造体や直和型のメンバーが不正な場合に、クラッシュしないようにしました ([#1228(英語)](https://github.com/carp-lang/Carp/issues/1228))。
- feat: HTML 形式のローカルドキュメントを追加しました ([#1229(英語)](https://github.com/carp-lang/Carp/issues/1229))。
- feat: `address` を特殊形式から削除し、`Pointer.address` に変更しました ([#1223(英語)](https://github.com/carp-lang/Carp/issues/1223))。
- feat: `Dynamic.get-env` と `Dynamic.set-env` を追加しました ([#1227(英語)](https://github.com/carp-lang/Carp/issues/1227))。
- fix: `aupdate` と `aupdate!` を、ほかの更新関数と統一しました ([#1220(英語)](https://github.com/carp-lang/Carp/issues/1220))。
- fix: 関数の仮引数でコマンドをシャドーイングできるようにしました ([#1217(英語)](https://github.com/carp-lang/Carp/issues/1217))。
- Fix: グローバルなコマンドのシャドーイングと、`let` の束縛における再帰を許可しました ([#1214(英語)](https://github.com/carp-lang/Carp/issues/1214))。
- fix: 型が不正な場合に、検証処理がクラッシュしないようにしました ([#1208(英語)](https://github.com/carp-lang/Carp/issues/1208))。
- fix: `set!` で型の付いていない形式を型チェックしないようにしました ([#1209(英語)](https://github.com/carp-lang/Carp/issues/1209))。
- fix: 再帰呼び出しに型を正しく割り当てるようにしました ([#1210(英語)](https://github.com/carp-lang/Carp/issues/1210))。
- fix: 具体化の際に名前が衝突しないよう、型変数の名前を変更しました ([#1212(英語)](https://github.com/carp-lang/Carp/issues/1212))。
- refactor: `Env` モジュールを整理し、モジュール内に型環境を格納するようにしました ([#1207(英語)](https://github.com/carp-lang/Carp/issues/1207))。
- feat: `Unsafe.C.asm` を追加しました ([#1206(英語)](https://github.com/carp-lang/Carp/issues/1206))。
- fix: 連続する複数の空白に対する `String.words` の動作を修正しました ([#1205(英語)](https://github.com/carp-lang/Carp/issues/1205))。
- feat: `Array.map-reduce` を追加しました ([#1201(英語)](https://github.com/carp-lang/Carp/issues/1201))。
- feat: 表示を整形する際に、型変数に ASCII 文字を使うようにしました ([#1195(英語)](https://github.com/carp-lang/Carp/issues/1195))。
- feat: キーワードをシンボルとして扱うようにしました ([#1190(英語)](https://github.com/carp-lang/Carp/issues/1190))。
- feat: `Char.to-byte` と `Char.from-byte` を追加しました ([#1187(英語)](https://github.com/carp-lang/Carp/issues/1187))。
- feat: `Maybe` と `Result` に `when` 関数群を追加しました ([#1180(英語)](https://github.com/carp-lang/Carp/issues/1180))。
- fix: 動的なクロージャ (closures) がグローバル環境を変更できるようにしました ([#1184(英語)](https://github.com/carp-lang/Carp/issues/1184))。
- refactor: 評価エラーを別のモジュールに移しました ([#1158(英語)](https://github.com/carp-lang/Carp/issues/1158))。
- feat: C コンパイラのディレクティブを出力するマクロを追加しました ([#1182(英語)](https://github.com/carp-lang/Carp/issues/1182))。
- fix: 登録した型のパスを修飾しないようにしました ([#1172(英語)](https://github.com/carp-lang/Carp/issues/1172))。
- feat: C コードそのものの出力をサポートしました ([#1178(英語)](https://github.com/carp-lang/Carp/issues/1178))。
- feat: `defn-` と `def-` マクロを追加しました ([#1174(英語)](https://github.com/carp-lang/Carp/issues/1174))。
- feat: 動的な `Map` 型を追加しました ([#1168(英語)](https://github.com/carp-lang/Carp/issues/1168))。
- fix: `carp-init-globals` の型を修正しました ([#1169(英語)](https://github.com/carp-lang/Carp/issues/1169))。
- feat: 単一化 (unification) の失敗時に、型変数の表示を整えるようにしました ([#1167(英語)](https://github.com/carp-lang/Carp/issues/1167))。
- fix: ベンチマークを再び追加しました ([#1166(英語)](https://github.com/carp-lang/Carp/issues/1166))。

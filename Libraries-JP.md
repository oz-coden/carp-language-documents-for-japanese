# ライブラリ (Libraries)

原文: [Libraries.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Libraries.md)

翻訳元のコミットは `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` です。
この文書は Carp の開発者・貢献者による英語原文を日本語に翻訳・編集した非公式の文書です。
翻訳方針は [TRANSLATION.md](TRANSLATION.md)、採用語は [GLOSSARY.md](GLOSSARY.md) を参照してください。

## ライブラリとモジュールの利用 (Working with libraries and modules)

Carp には Core という標準ライブラリが付属しています。[ソースコード(英語)](https://github.com/carp-lang/Carp/tree/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/core/) を参照できます。
標準ライブラリは複数のモジュールで構成されています。
ほとんどのモジュールについて、[オンライン(英語)](http://carp-lang.github.io/carp-docs/core/core_index.html) と [ローカル(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/core/core_index.html) の両方でドキュメントを利用できます。

> 訳注: 原文のローカル向けリンク先 `docs/core/core_index.html` は、固定コミットには含まれていません。ローカルで生成するドキュメントについては [生成手順(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/core/README.md) を参照してください。

大部分のモジュールは既定で読み込まれます。詳しくは [Core.carp(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/core/Core.carp) を参照してください。
環境変数 `CARP_DIR` が [正しく設定](Install-JP.md#carp_dir-の設定-setting-the-carp_dir) されていれば、残りのライブラリも `load` コマンドで簡単に読み込めます。例えば、`Bench` モジュールを使えるようにするには、次のようにします。

```clojure
(load "Bench.carp")
```

`Bench` モジュールの関数を使う際には、引き続き `(Bench.bench fib)` のように関数名の前にモジュール名を付ける必要があります。これを省略するには、さらに `(use Bench)` を実行します。

あるモジュールにどのような関数が含まれているかを確認するには、`info` コマンドを使います。

```clojure
(info Bench)
```

外部ライブラリは、ファイルシステム上の相対パスまたは絶対パスを指定して読み込めます。ライブラリをより広く利用できるようにするには、Carp プロジェクトの検索パスに追加できます。検索パスは REPL で `:p` を実行すると確認できます。例えば、`(load "NCurses.carp")` だけで読み込めるように NCurses ライブラリを追加するには、次のようにします。

```clojure
(Project.config "search-path" "~/Projects/carp-ncurses")
```

この設定を [profile.carp](Manual-JP.md#プロファイルの設定-profile-settings) に記述すると、すべてのプロジェクトに適用できます。

## Git 経由での読み込み (Loading via git)

次のように、Git 経由でライブラリを読み込むこともできます。

```clojure
(load "git@github.com:hellerve/anima.carp@master")
```

これにより、[Anima(英語)](https://github.com/hellerve/anima) ライブラリを `~/.carp/libs/<library>/<tag>` にダウンロードし、その中の `anima.carp` ファイルを読み込みます。安定したバージョンのライブラリを使うには、`@master` ではなく Git のタグを指定してください。

自分のライブラリをこの方法で読み込めるようにするには、ライブラリと同じ名前のファイル (上の例では `anima.carp`) か、エントリーポイント (entrypoint) となる `main.carp` という名前のファイルを用意します。

非公開リポジトリでは、SSH 経由の読み込みだけがサポートされていることに注意してください。公開リポジトリでは HTTPS を使えます。

```clojure
(load "https://github.com/hellerve/anima@master")
```

## ドキュメント (Documentation)

REPL で `save-docs` を実行すると、複数のモジュールの HTML ドキュメントを生成できます。

```clojure
> (save-docs Int Float String)
```

標準ライブラリ全体のドキュメントの更新については [README(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/core/README.md) を、ドキュメント生成ツールの設定例については [生成プログラム(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/core/generate_core_docs.carp) を参照してください。

## 自動生成される API ドキュメント (Auto generated API documentation)

- [Carp 標準ライブラリのオンラインドキュメント(英語)](http://carp-lang.github.io/carp-docs/core/core_index.html)
- [Carp 標準ライブラリのローカルドキュメント(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/core/core_index.html)
- [SDL(英語)](http://carp-lang.github.io/carp-docs/sdl/SDL_index.html)

## 外部ライブラリの例 (Some External Libraries)

- [Anima(英語)](https://github.com/hellerve/anima): シンプルな描画・アニメーション用フレームワークです。
- [Stdint(英語)](https://github.com/hellerve/stdint): `stdint.h` で定義された型のラッパー (wrapper) です。
- [Socket(英語)](https://github.com/hellerve/socket): C のソケットのラッパーです。
- [Physics(英語)](https://github.com/hellerve/physics): phys.js の移植版です。
- [NCurses(英語)](https://github.com/eriksvedang/carp-ncurses): [ncurses(英語)](https://www.gnu.org/software/ncurses/)
- [Curl(英語)](https://github.com/eriksvedang/carp-curl): Curl ライブラリのシンプルなバインディング (binding) です。

Carp のパッケージ一覧は [Carpentry(英語)](https://github.com/carpentry-org) を参照してください。掲載数は増え続けています。

ここで紹介したいライブラリがあれば、ぜひ Carp 本体に PR を送ってください。

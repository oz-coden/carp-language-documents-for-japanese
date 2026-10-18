# インストール (Installation)

原文: [Install.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Install.md)

翻訳対象は 2026-10-19 確認時点の原文です。対象コミットは `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` です。
この文書は Carp の開発者・貢献者による英語原文を日本語に翻訳・編集した非公式の文書です。
翻訳方針は [TRANSLATION.md](TRANSLATION.md)、採用語は [GLOSSARY.md](GLOSSARY.md) を参照してください。

## 最新リリース (Latest release)

[Carp のリリース一覧(英語)](https://github.com/carp-lang/Carp/releases) を参照してください。

## ソースからの Carp 実行ファイルのビルド (Building the Carp executable from source)

1. 比較的新しいバージョンの [Stack(英語)](https://docs.haskellstack.org/en/stable/README/) がインストールされていることを確認します。
2. Carp のリポジトリを自分のマシンにクローンします。
3. プロジェクトのルートディレクトリで `stack build` を実行します。
4. `stack install` を実行すると、システム上で簡単に呼び出せるように Carp のコマンドラインツールがインストールされます。
5. Stack が実行ファイルをインストールするディレクトリが `PATH` に含まれていることを確認します。例えば、`export PATH=~/.local/bin:$PATH` と設定します。

## `CARP_DIR` の設定 (Setting the CARP_DIR)

システム上のどこからでも `carp` を実行するには、実行ファイルがコアライブラリやその他のファイルを見つけられる必要があります。
環境変数 `CARP_DIR` が Carp リポジトリのルートを指すように設定します。

例えば、`.bashrc` などに次の内容を追加します。

```bash
export CARP_DIR=~/Carp/
```

これで、どこからでも Carp を起動できるはずです。

```bash
$ carp
```

## POSIX 環境での UTF-8 対応の `LC_CTYPE` ロケールの確認 (Ensuring an UTF-8 aware LC_CTYPE locale in POSIX environments)

`carp` の対話的な REPL で UTF-8 を正しく扱うには、POSIX に対応したすべての環境で、環境変数 `LC_CTYPE` に UTF-8 対応のロケール (locale) を設定し、エクスポートする必要があります。これには Linux、macOS、さらには Windows 10 上で動く Emacs の eshell も含まれます。なお、`carp` が生成するバイナリは、常に UTF-8 を正しく扱います。

例えば、`.bashrc` などに次の内容を追加します。

```bash
export LC_CTYPE=C.UTF-8
```

環境変数 `LC_ALL` が設定されている場合、その値が `LC_CTYPE` より優先されることに注意してください。
そのため、`LC_ALL` を `unset` で解除するか、UTF-8 対応の値を設定してエクスポートするとよいでしょう。
`LC_ALL` と `LC_CTYPE` の値は、`locale` コマンドで確認できます。

## C コンパイラ (C compiler)

`carp` 実行ファイルは、C コードを含む単一のファイル `main.c` を出力し、外部の C コンパイラでコンパイルしようとします。
macOS と Linux では、既定のコンパイラは `clang` なので、インストールされていることを確認してください。macOS では、開発者向けツールを含めて Xcode をインストールする方法が推奨されます。

Windows で Carp が既定で使用する C コンパイラは `clang-cl.exe` です。コードのコンパイルには Clang を使い、リンクには Visual Studio のリンカーを使います。Windows で簡単に環境を構築するには、パッケージマネージャーの [Scoop(英語)](https://scoop.sh/) を使って LLVM をインストールする方法があります。また、C/C++ アドオンを含めて Visual Studio がインストールされていることも確認してください。Carp を使うために WSL (Windows Subsystem for Linux) は *必要ありません*。

別のコンパイラを使いたい場合は、次のようにビルドコマンドを具体的に設定できます。

```clojure
(Project.config "compiler" "gcc --important-flag")
```

## SDL、GLFW など (SDL, GLFW, etc)

グラフィックス、サウンド、対話操作を扱うサンプルを使うには、システムに次のライブラリをインストールする必要があります。

- [SDL 2(英語)](https://www.libsdl.org/download-2.0.php): クロスプラットフォームのゲーム・対話操作用ライブラリです。
- [SDL_image 2(英語)](https://www.libsdl.org/projects/SDL_image/): 画像を扱うための補助機能です。
- [SDL_ttf 2(英語)](https://www.libsdl.org/projects/SDL_ttf/): フォントの描画を行います。
- [SDL_mixer 2(英語)](https://www.libsdl.org/projects/SDL_mixer/): 音声の再生を行います。
- [glfw(英語)](http://www.glfw.org): OpenGL または Vulcan のレンダリングコンテキスト (rendering context) を作成します。

> 訳注: 原文は `Vulcan` と表記していますが、文脈と GLFW の説明から、グラフィックス API の `Vulkan` を指すと考えられます。

macOS と Linux では、インクルードパスやリンクフラグを扱うために [pkg-config(英語)](https://www.freedesktop.org/wiki/Software/pkg-config/) を使います。正しくインストールされ、外部ライブラリを見つけられるように設定されていることを確認してください。

これらのバインディング (binding) がうまく動かない場合は、Carp の開発者に知らせてください。できる限り確実に動作するようにしていますが、依存関係の管理では特殊な条件で問題が生じることがよくあります。[Carp の Issue(英語)](https://github.com/carp-lang/Carp/issues) の作成や、[Gitter チャンネル(英語)](https://gitter.im/carp-lang/Carp) での質問も歓迎します。

## Windows 向けの補足 (Footnote for Windows)

mingw64 を使って `clang` をインストールできますが、`clang` が正しいヘッダーを見つけられるように、シェルを起動するたびに `vcvarsall.bat amd64` または `vcvarsall.bat x86` も実行するとよいでしょう。
詳しくは [Issue #700(英語)](https://github.com/carp-lang/Carp/issues/700) または [Issue #1323(英語)](https://github.com/carp-lang/Carp/issues/1323) を参照してください。

また、Windows で `carp` を使ってファイルをコンパイルするときは、次の点を確認する必要があります。

- ファイルの文字エンコーディングが ANSI または UTF-8 であること。UTF-8-BOM など、ほかの文字エンコーディングでは動作しません。
- 改行に Unix (LF) または Windows (CR LF) を使うこと。Macintosh (CR) の改行では動作しません。

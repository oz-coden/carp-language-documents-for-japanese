# コードの実行方法 (How to run code)

原文: [HowToRunCode.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/HowToRunCode.md)

翻訳元のコミットは `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` です。
この文書は Carp の開発者・貢献者による英語原文を日本語に翻訳・編集した非公式の文書です。
翻訳方針は [TRANSLATION.md](TRANSLATION.md)、採用語は [GLOSSARY.md](GLOSSARY.md) を参照してください。

この文書は、Carp を使い始めたばかりの方、特に [サンプル(英語)](https://github.com/carp-lang/Carp/tree/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/examples) を試してみたい方を対象としています。

## 前提条件 (Prerequisites)

[Carp コンパイラと依存関係のインストール](Install-JP.md) が済んでいて、エラーメッセージを出さずに起動できることを確認してください。

次のように表示されるはずです。

```text
$ carp
Welcome to Carp X.Y.Z
This is free software with ABSOLUTELY NO WARRANTY.
Evaluate (help) for more information.
鲤
```

最後の行の `鲤` は [REPL(英語)](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop) のプロンプト (prompt) で、Carp がコマンドの入力を待っていることを意味します。

## REPL からのコードの実行 (Running code from the REPL)

次のようにコードを読み込めます。

```bash
鲤 (load "some_file.carp")
```

ファイルへのパスは、`carp` を起動した場所からの相対パスで指定します。または、そのファイルが [検索パス `search-path`(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Libraries.md) から見つかる場所にある必要があります。
コードのまとまりを REPL に貼り付けることもできます。複数のトップレベルの式を含んでいても構いません。

ビルドして実行するには、まず次を実行します。

```bash
鲤 (build)
```

続けて、次を実行します。

```
鲤 (run)
```

## ターミナルからのコードの実行 (Running code from the terminal)

REPL を使わず、より従来の「コンパイルして実行する」方法を使いたい場合は、次のようにします。

```bash
$ carp some_file.carp -x
```

`carp` に引数として指定したファイルは、すべて読み込まれます。これは REPL を起動するときにも使えます。
`-x` フラグは、コードをすぐにコンパイルして実行し、その後に終了することを指定します。

実行ファイルをビルドするだけなら、代わりに `-b` を使います。

```bash
$ carp some_file.carp -b
```

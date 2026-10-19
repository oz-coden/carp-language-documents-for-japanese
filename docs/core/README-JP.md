# 標準ライブラリのドキュメント生成 (Generating Standard Library Documentation)

原文: [README.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/core/README.md)

翻訳元のコミットは `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` です。
この文書は Carp の開発者・貢献者による英語原文を日本語に翻訳・編集した非公式の文書です。
翻訳方針は [TRANSLATION.md](../../TRANSLATION.md)、採用語は [GLOSSARY.md](../../GLOSSARY.md) を参照してください。

Carp 標準ライブラリのリファレンスは [オンライン(英語)](http://carp-lang.github.io/carp-docs/core/core_index.html) で参照できますが、Carp のインストール先にある `docs/core` ディレクトリにも、ローカルのコピーが含まれているはずです。

[短い Carp プログラム(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/core/generate_core_docs.carp) を実行して、ローカルのコピーを更新できます。このプログラムは、`./docs/core` ではなく Carp のインストール先ディレクトリから実行する必要があることに注意してください。

```
carp -x ./docs/core/generate_core_docs.carp
```

> 訳注: 固定コミットには、生成済みの `docs/core/core_index.html` は含まれていません。上のコマンドは、本家の Carp インストール先でドキュメントを生成・更新するためのものです。

# 本家への貢献ガイド (Contributing Guide)

原文: [Contributing.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Contributing.md)

翻訳元のコミットは `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` です。
この文書は Carp の開発者・貢献者による英語原文を日本語に翻訳・編集した非公式の文書です。
翻訳方針は [TRANSLATION.md](TRANSLATION.md)、採用語は [GLOSSARY.md](GLOSSARY.md) を参照してください。

Carp への貢献を検討してくださり、ありがとうございます！

この文書は、現在は開発者による貢献を中心に説明していますが、あらゆる形の貢献を歓迎します。

## コミュニティ (Community)

まずは、[Carp の Gitter チャンネル(英語)](https://gitter.im/carp-lang/Carp) に参加するのがお勧めです。

> 訳注: このガイドと Gitter の案内は、Carp 本家への貢献に関するものです。日本語訳への貢献は、[このリポジトリの貢献手順](CONTRIBUTING.md) を参照してください。日本語訳や訳注の問題は、本家ではなく [このリポジトリの Issue](https://github.com/oz-coden/carp-language-documents-for-japanese/issues) へ報告してください。翻訳の問題か原文の問題か判断できない場合も、まずこちらへ相談してください。

## コンパイラを理解する (Understanding the Compiler)

Carp コンパイラの内部をやさしく紹介する [hacking.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/hacking.md) を参照してください。

## リポジトリへのコミット (Committing to the repo)

[Conventional Commits(英語)](https://www.conventionalcommits.org) に従っています。コミットメッセージが規約に従っていることを確認するための `commit-msg` フックがあるので、最初にコミットする前に `./scripts/git-hooks/setup.sh` を実行し、フックを設定しておいてください。

## ライセンス (License)

Carp は現在、ASL 2.0 ライセンスの条件の下で公開されています。

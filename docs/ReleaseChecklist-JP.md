# リリースチェックリスト (Release Checklist)

原文: [ReleaseChecklist.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/ReleaseChecklist.md)

翻訳元のコミットは `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` です。
この文書は Carp の開発者・貢献者による英語原文を日本語に翻訳・編集した非公式の文書です。
翻訳方針は [TRANSLATION.md](../TRANSLATION.md)、採用語は [GLOSSARY.md](../GLOSSARY.md) を参照してください。

> 訳注: 本書は Carp 本家のリリース手順です。以下のファイルやコマンドは、本家リポジトリを対象としています。

次の作業を、おおむねこの順番で行ってください。

## 1. Cabal プロジェクトのバージョンを更新する (1. Update Cabal project version)

[CarpHask.cabal(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/CarpHask.cabal) の 2 行目を参照してください。

## 2. REPL の「Welcome to Carp X.Y.Z」メッセージを更新する (2. Update the "Welcome to Carp X.Y.Z" REPL message)

[Main.hs(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/app/Main.hs) を参照してください。

> 訳注: 原文のリンク先は `App/Main.hs` ですが、対象コミットのパスは `app/Main.hs` です。この訳文のリンクは、実在する後者を指しています。

## 3. README.md の紹介文を更新する (3. Update the blurb in README.md)

原文参照: [README.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/README.md)

## 4. 変更履歴を更新する (4. Update the changelog)

原文参照: [CHANGELOG.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/CHANGELOG.md)

日本語訳は [変更履歴](../CHANGELOG-JP.md) を参照してください。

## 5. master でコミットを作成する (5. Make a commit on master)

```bash
$ git add .
$ git commit -m "build: Release X.Y.Z"
```

## 6. コミットにタグを付けてプッシュする (6. Tag the commit and push it)

```bash
$ git tag vX.Y.Z
$ git push --tags
```

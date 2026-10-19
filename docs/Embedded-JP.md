# 組み込み開発 (Embedded)

原文: [Embedded.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/Embedded.md)

翻訳元のコミットは `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` です。
この文書は Carp の開発者・貢献者による英語原文を日本語に翻訳・編集した非公式の文書です。
翻訳方針は [TRANSLATION.md](../TRANSLATION.md)、採用語は [GLOSSARY.md](../GLOSSARY.md) を参照してください。

組み込み機器 (embedded device) 向けのプログラミングは、少し砂漠での生活に似ています。何もかもが乏しく、常に節約しなければならず、日なたも避けたほうがよいのです。

この文書では、Carp でリソースを節約する方法を案内します。そのためには、まず何を最も重視するかを明らかにする必要があります。実行ファイルのサイズでしょうか。実行時間の制約が厳しいコードがあるのでしょうか。メモリの割り当てを避けたいのでしょうか。こうした問いに答えが出れば、このガイドが目標の達成に役立ちます。

Carp は C にコンパイルされるため、C と同じ考慮事項、工夫、考え方の多くが当てはまります。必要なフラグがすでに分かっていれば、それは何よりです。Carp でも、おそらくそのまま使えるでしょう。それでも、Carp が用意しているツールを知っておけば、より円滑に開発を進められるはずです。

## 百聞は一見に…… (A picture is worth...)

何ができるかのイメージをつかみ、興味を持ってもらうために、写真を紹介します。

![Arduboy で動作する Carp](https://raw.githubusercontent.com/carp-lang/Carp/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/carp_on_arduboy.jpg)

## 基礎 (Fundamentals)

コンパイラを思いどおりに動かすには、利用できる設定項目をしっかり理解する必要があります。この節では、プロジェクトをコンパイルできるようにするために、どのような設定ができるかを概観します。

### コンパイラ (Compiler)

コンパイラに指示を出すための動的関数がいくつかあります。次に一覧を示します。

```clojure
; 使用する C コンパイラの実行ファイルを Carp に指定する
(Project.config "compiler" "mycompiler")

; コンパイラの呼び出しに、このフラグを追加するよう Carp に指示する
(add-cflag "-myflag")

; コンパイラの呼び出しに、このライブラリ用フラグを追加するよう Carp に指示する
(add-lib "-mylibflag")

; ライブラリの libs と cflags を取得するために pkg-config を実行するよう Carp に指示する
(add-pkg "mypkg")
```

### クロスコンパイル (Cross-compiling)

組み込みシステム (embedded system) では、クロスコンパイラ (cross-compiler) を使うのが一般的です。その使い方は、マニュアルの [クロスコンパイル](Manual-JP.md#クロスコンパイル-cross-compiling) の節を参照してください。

### コンパイル時の条件付きコード (Compile-time conditional code)

ビルドを行っているホストシステム (host system) について調べるためのマクロがいくつかあります。

手始めに役立つ関数を紹介します。

```clojure
; ホストの OS を返す
(host-os)

; ホストのアーキテクチャのビット幅 (例えば 32 ビットや 64 ビット) を返す
(host-bit-width)
```

ただし、ほとんどの場合、知りたいのは実行対象となるターゲットプラットフォーム (target platform) の詳細でしょう。

```clojure
; ターゲットのアーキテクチャを返す
(target-arch)

; ターゲットの OS を返す
(target-os)

; ターゲットの ABI を返す
(target-abi)

```

> 訳注: 対象コミットでは、`target-arch`、`target-os`、`target-abi` は関数ではなく、`defdynamic` で定義された値です。参照するときは、`(target-arch)` のような呼び出し形式ではなく、`target-arch`、`target-os`、`target-abi` と記述します。[ターゲット情報の定義(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/core/Platform.carp#L11-L18)

条件付きコードに使えるマクロは、[`Macros.carp`(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/core/Macros.carp) にあります。ターゲットに基盤となる OS がなければ、`freestanding` ターゲット向けに独自のマクロを書くことになるでしょう。

### 困ったときの対処法 (The Way Out)

独自のリンカースクリプト (linker script) を使うなど、特殊な工夫が必要になる場合もあります。そのようなときは、Carp には C コードの生成だけを指示し、あとの処理を自分で行うのが最善なこともよくあります。Carp に `--generate-only` を指定すると、この方法を使えます。

通常はプレリュード (prelude) が読み込むファイルの一部を読み込ませず、代わりにコアライブラリを読み込む独自のファイルを作成しなければならない場合もあります。これには `--no-core` を使います。そのうえで、[標準のプレリュード(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/core/Core.carp) を独自のファイルのひな型にできます。

## 最適化の対象 (What to optimize for)

### バイナリのサイズ (Binary size)

Carp は、既定ではバイナリのサイズを最適化しません。[リンク時最適化(英語)](https://wiki.debian.org/LTO) (Link Time Optimization、LTO) を利用し、コンパイラにサイズを重視した最適化を指示すると、通常はメモリ使用量をかなり削減できます。GCC や Clang を使っている場合は、`(add-cflag "-Os")` を指定します。

### 実行速度 (Speed)

速度は、ほかの要素ほど重要でないこともよくあります。それでも、さらに数ミリ秒を削りたい場合は、最高の最適化設定を使うのが適切かもしれません。多くの場合、`-O3` と Carp のフラグ `--optimize` を併用します。もちろん、これで何でも解決するわけではありません。通常、速度はコンパイラの動作よりも、コードの構造に大きく左右されます。メモリの割り当て、コピー (copies)、キャッシュミス (cache miss) を避けるほうが、最適化器を使うよりも速度の向上につながるでしょう。

### メモリの割り当て (Allocations)

メモリの割り当てを避けるには、いくつかの工夫があります。文字列リテラルは、既定ではメモリを割り当てるのではなく、バイナリに埋め込まれます。コピーを行わずに済むなら、これは大きな利点になります。同様に、静的配列 (static array) も、メモリの割り当てを避けるために使えます。リテラルには `$[]` を使います。ただし、サイズと構造がコンパイル時に分かっている必要があります。

開発やデバッグの際にメモリの割り当てをログに記録するには、Carp コンパイラに `--log-memory` を渡し、プログラムの先頭に `(Debug.log-memory-balance! true)` という形式を置きます。これですべての割り当てがログに記録されるので、気付かないうちに発生していた割り当てを突き止めやすくなります。

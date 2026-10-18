# C との相互運用 (C Interop)

原文: [CInterop.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/CInterop.md)

翻訳対象は 2026-10-19 確認時点の原文です。対象コミットは `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` です。
この文書は Carp の開発者・貢献者による英語原文を日本語に翻訳・編集した非公式の文書です。
翻訳方針は [TRANSLATION.md](TRANSLATION.md)、採用語は [GLOSSARY.md](GLOSSARY.md) を参照してください。

この文書では、[言語ガイドの C との相互運用](LanguageGuide-JP.md#c-との相互運用-c-interop) で扱った内容をさらに詳しく説明します。

## 目次 (Content)

- [Carp による識別子の生成](#carp-による識別子の生成-how-carp-generates-identifiers)
- [メモリ管理の対象となる型](#メモリ管理の対象となる型-managed-types)
  - [文字列](#文字列-string)
  - [配列](#配列-array)
- [Carp への C コードの埋め込み](#carp-への-c-コードの埋め込み-embedding-c-code-in-carp)
  - [`deftemplate` による定義](#deftemplate-による定義-deftemplate)
    - [基本的な例](#基本的な例-basic-example)
    - [ジェネリクス](#ジェネリクス-generics)
  - [C コードの直接出力](#c-コードの直接出力-unsafeemit-c)
  - [C コードの先行挿入](#c-コードの先行挿入-unsafepreproc)
  - [型の登録](#型の登録-registering-types)
- [コールバック](#コールバック-callbacks)
- [Headerparse](#headerparse)

## Carp による識別子の生成 (How Carp generates identifiers)

関数や `def` を作成するとき、C 側でどのような識別子が生成されるかを知っておくと役立つことがあります。例を示します。

```clojure
(def a-def 100)
; => a_MINUS_def

(defn hello [] (println* "Hello"))
; => hello

(sig true? (Fn [Bool] Bool))
(defn true? [b] b)
; true_QMARK_

(defmodule Reverse
  (defn hello [] (println* "Goodbye"))
  ; => Reverse_hello
  (defmodule ReReverse
    (defn hello [] (println* "Hello"))))
    ; => Reverse_ReReverse_hello

; ジェネリックな型シグネチャ
(sig print-first-and-add (Fn [(Ref (Array a)) b b] b))
(defn print-first-and-add [arr x y]
 (do
   (println* (Array.unsafe-first arr))
   (+ x y)))
; 呼び出されるまでコードは生成されない

(print-first-and-add &[1] 1 1)
; => print_MINUS_first_MINUS_and_MINUS_add__int_int
(print-first-and-add &[@"hello"] 2l 40l)
; => print_MINUS_first_MINUS_and_MINUS_add__String_Long
```

上の例から、C コードを生成する前に Carp が識別子をどのように変換するかが分かるでしょう。詳しく見ていきます。Carp は C の識別子に使えない文字を、その文字を表す文字列に置き換えます (`- => _MINUS_`、`? => _QMARK_` など)。
モジュール内の識別子には、モジュール名を接頭辞として付けます。
関数の引数がジェネリックな場合は、識別子の末尾に型を付けます。このような識別子は、関数が使われるまで生成できません。関数がジェネリックになり得るものの、そうしたくない場合は、`true?` の例のように、ジェネリックではない型シグネチャを付けることで Carp に関数を生成させられます。

この処理は *名前マングリング (mangling)* と呼ばれます。Carp では有効でも C では無効な識別子から、不正な C コードが生成されるのを防ぐために必要です。

### Carp の既定の C 識別子名の上書き (Overriding Carp's default C identifier names)

既存の C ライブラリのバインディング (binding) を Carp で作成する際、C で宣言されている識別子をそのまま再現しなければならないのは不便です。例えば、名前マングリングによって生成される識別子には接頭辞が付くため、おそらく正しい識別子にならず、Carp のバインディングをモジュールで囲めなくなります。
既存ライブラリのバインディングを作るたびに C の識別子を正確に再現するのは不便で手間がかかります。そのため、`register` と `register-type` には、使用する識別子を指定するオプションの引数があります。

```clojure
(defmodule CURL
  (register-type HttpPost "curl_httppost")
  (register form-free (Fn [(Ref HttpPost)] ()) "curl_formfree"))
```

これにより、呼び出す既存の C ライブラリの識別子に正しく対応する識別子を生成しつつ、Carp のコードを自由に構成できます。この例では cURL のバインディングを `CURL` モジュールで囲んでいます。
例えば、Carp の識別子 `form-free` は通常なら名前マングリングの対象となり、`form_MINUS_free` として出力されますが、上書き用の引数を指定すると、代わりに `curl_formfree` として出力されます。

同様に、すべて Carp で定義したコードについても、Carp が生成する C の識別子を上書きできます。例えば、既存の C プログラムの安全性が特に重要なコードを Carp に移し、そこから生成された安全な C コードを元の C プログラムから呼び出したい場合があります。Carp のコードで入れ子になったモジュール、独自の型、識別子内の特殊文字を多用していると、呼び出しが煩雑になることがあります。

`c-name` メタフィールドを使うと、ある定義に対して Carp が生成する C の識別子を明示的に設定できます。これにより、生成される C コードが読みやすくなり、ほかの言語からも呼び出しやすくなります。例えば、次の定義と `c-name` の呼び出しがあるとします。

```clojure
(defn foo-bar [] 2)
(c-name foo-bar "foo_bar")
```

Carp は C の出力で、既定の `foo_MINUS_bar` の代わりに、対応する識別子 `foo_bar` を生成します。

## メモリ管理の対象となる型 (Managed types)

Carp では、`String` や `Array` などは *メモリ管理の対象となる型 (managed type)* です。ヒープにメモリが割り当てられ、スコープを抜けるとコンパイラがそのメモリを自動的に解放します。ここでは、こうした型と C の間で値をやり取りする方法を見ていきます。

### 文字列 (String)

`char*` を要求する C 関数にメモリ管理の対象となる `String` を渡すには、`(Ref String)` を `(Ptr CChar)` に変換する `String.cstr` 関数を使えます。

```clojure
(register puts (Fn [(Ptr CChar)] ()))

(let [a-str @"A string."]
  (puts (String.cstr &a-str)))
(puts (String.cstr "Hello"))
```

利用者から C の型を隠したい場合もあるでしょう。

```clojure
(defmodule MyMod
  (hidden puts-c)
  (private puts-c)
  (register puts-c (Fn [(Ptr CChar)] ()) "puts")
  (defn puts [str-ref] (puts-c (String.cstr str-ref))))

(let [a-str @"A string."]
  (MyMod.puts &a-str))
(MyMod.puts "Hello")
```

---

受け取った `char*` をメモリ管理の対象となる `String` に変換したい場合は、`String.from-cstr` を使えます。この関数はメモリを割り当て、C の文字列の内容をコピーします。

```c
// static-str.h
char* returns_a_static_str() {
  return "Hello";
}
```

```clojure
(relative-include "static-str.h")

(register returns-a-static-str (Fn [] (Ptr CChar)) "returns_a_static_str")

(let [a-str (String.from-cstr (returns-a-static-str))]
  (println* (String.concat &[a-str @" " @"Carp"])))
```

---

呼び出す関数が文字列をヒープに割り当ててくれる場合もあります。その場合は、その関数がメモリ管理の対象となる `String` を返すと宣言できます。
ただし、これは安全でない可能性があります。文字列が実際にヒープに割り当てられており、使用するアロケータ (allocator) が Carp のものと同じであることを確認する必要があります。

```c
char* returns_a_heap_string() {
  char *hello = "Hello from the heap";
  char *str = malloc((strlen(hello)+1));
  strcpy(str, hello);
  return str;
}
```

```clojure
(relative-include "heap-string.h")

(register returns-a-heap-str (Fn [] String) "returns_a_heap_string")

(let [a-str (returns-a-heap-str)]
  (println* a-str))
```

C のコードを自分で書く場合は、`CARP_MALLOC` マクロを使うことで、Carp コンパイラと同じアロケータを使っていることを保証できます。

```c
char* returns_a_heap_string() {
  char *hello = "Hello from the heap";
  char *str = CARP_MALLOC((strlen(hello)+1));
  strcpy(str, hello);
  return str;
}
```

### 配列 (Array)

C の配列を引数に取る関数がある場合は、`Array.unsafe-raw` を使えます。

```c
int sum(int *arr, int len) {
  int acc = 0;
  for (int i = 0; i < len; i++) {
    acc += arr[i];
  }
  return acc;
}
```

```clojure
(relative-include "sum.h")

(register sum-c (Fn [(Ptr Int) Int] Int) "sum")

(let [ints [1 2 3]]
  (println* (sum-c (Array.unsafe-raw &ints) (Array.length &ints))))
```

ここでも、C の関数をそのまま使う代わりに、より Carp らしいインターフェースで包みたい場合があるでしょう。

```clojure
(relative-include "sum.h")

(defmodule MyMod
  (hidden sum-c)
  (private sum-c)
  (register sum-c (Fn [(Ptr Int) Int] Int) "sum")

  (sig sum (Fn [(Ref (Array Int))] Int))
  (defn sum [ints] (sum-c (Array.unsafe-raw ints) (Array.length ints))))

(MyMod.sum &[1 2 3])
```

---

呼び出し先の関数がデータの所有権を取得する場合は、`Array.raw` を使えます。渡されたポインタと、その中に含まれるメモリ管理の対象となる型の値に対して `free` を呼び出す責任は、呼び出し先の関数が負います。

```c
// printall.h
void println_all(char **arr, int len) {
  for (int i = 0; i < len; i++) {
    printf("%s\n", arr[i]);
    CARP_FREE(arr[i]);
  }
  CARP_FREE(arr);
}
```

```clojure
(relative-include "printall.h")

(register println-all (Fn [(Ptr String) Int] ()) "println_all")

(let [lines [@"One" @"Two" @"Three"]
      len (Array.length &lines)]
  (println-all (Array.raw lines) len))
```

## Carp への C コードの埋め込み (Embedding C code in Carp)

C ライブラリと連携する際、独自の C コードでライブラリの関数を包むと便利な場合があります。ヘッダーファイルにコードを書き、Carp 側からインクルードして `register` で登録するのも有効な方法です。

```c
// print.h
// String は Carp コアで定義される char* の別名
void print_that_takes_ownership(String str) {
  printf("%s", str);
  CARP_FREE(str);
}
```

```clojure
(relative-include "print.h")

(register print (Fn [String] ()) "print_that_takes_ownership")

(print @"Print this!")
```

ただ、C のコードを Carp のコードの近くに置いておきたい場合もあるでしょう。そこで `deftemplate` の出番です。

### `deftemplate` による定義 (`deftemplate`)

#### 基本的な例 (Basic example)

先ほどの例は、代わりに次のようにも定義できます。

```clojure
(deftemplate print (Fn [String] ())
                   "void $NAME(String str)"
                   "$DECL {
                     printf(\"%s\", str);
                     CARP_FREE(str);
                   }")

(print @"Print this!")
```

ここで何が行われているかを見ていきます。

- `deftemplate` の **第 1 引数** は、関数を参照するための名前です。
- **第 2 引数** は型シグネチャで、先ほどの `register` の呼び出しで指定したものと同じです。
- **第 3 引数** は関数宣言で、生成される C ファイルの先頭に挿入されます。
- **最後の引数** は関数定義です。

さらに、次の 2 点に注目してください。

- `$NAME` は、関数に付けた名前と、その関数が定義されているモジュールから決まる変数です。ほかのモジュールにある `print` 関数との名前の衝突を心配する必要はありません。
- 関数を定義するとき、`$DECL` は第 3 引数で渡した宣言に置き換えられます。

このように、`deftemplate` を使うと Carp と C のコードを近くに置き、全体としてコードの量を減らせます。しかし、その真価は別のところにあります。

#### ジェネリクス (Generics)

2 つの数を足す関数を書きたいとします。数値の型ごとに別の関数を書くのは手間がかかります。`deftemplate` がどのように役立つかを見ていきます。

```clojure
(deftemplate add (Fn [a a] a)
                 "$a $NAME($a x, $a y)"
                 "$DECL {
                   return x + y;
                 }")

(add 1 2)
(add 20l 22l)
(add 2.0f 5.0f)

; 型が異なるため、この呼び出しはできない
; (add 2.0f 22l)
```

Carp では、型シグネチャでジェネリック型を使えます。この例では `a` がそれに当たります。C のコードでは、型シグネチャで使ったジェネリックな型の名前の前に `$` を付けると、その型を参照できます。Carp は、異なる型でテンプレートを使用するたびに、それぞれ別の関数を生成します。

注意してください。この関数を呼び出す際には、Carp コンパイラが保証する型安全性がすべて失われています。C コンパイラが問題を検出してくれることを期待するしかありません。

``` clojure
(deftemplate add (Fn [a a] a)
                 "$a $NAME($a x, $a y)"
                 "$DECL {
                   return x + y;
                 }")

(add @"A string" @" another string")
```

幸い、この例では Clang が次のエラーを出しますが、それに頼らない方がよいでしょう。

```
out/main.c:9153:29: error: invalid operands to binary expression ('String' (aka 'char *') and 'String')
                   return x + y;
                          ~ ^ ~
1 error generated.
```

### C コードの直接出力 (`Unsafe.emit-c`)

`deftemplate` は柔軟で、ほとんどの用途には十分ですが、必要なことを実現できない場面もあります。例えば、C11 の `static_assert` など、C のマクロには引数に文字列リテラルを要求するものがあります。`deftemplate` ではこれを実現できません。
そのような場合は、`Unsafe.emit-c` を使って Carp コンパイラが生成する C コード内に文字列をそのまま出力できます。`emit-c` は、`static_assert` の呼び出しのような用途に適しています。`static_assert` が `static-assert` という名前で `register` によって登録されているとすると、次のように `emit-c` を使い、コンパイラが生成する C コードで文字列リテラルが渡されるようにできます。

```
(register static-assert (Fn [a C] ()))

(static-assert 0 (Unsafe.emit-c "\"foo\""))
```

これに対応する、次の C コードが生成されます。

```
static_assert(0, "foo")
```

`emit-C` は `C` 型の値を返します。`C` は、Carp 内で C コードそのものを表す特殊な型です。

> 訳注: 原文ではここだけ `emit-C` と表記されていますが、この節の見出しや例にある `Unsafe.emit-c` を指すと考えられます。また、上の `register` の例には C 側の名前 `static_assert` の明示的な指定がありません。掲載コードと出力例は原文のままです。

### C コードの先行挿入 (`Unsafe.preproc`)

Carp コンパイラは、関数を呼び出す前にその依存先が利用できるような順序で C コードを出力します。ときには、Carp コンパイラの出力よりも前に C コードを含めたいことがあります。例えば、C コンパイラにプリプロセッサディレクティブ (preprocessor directive) を渡したい場合です。`Unsafe.preproc` 関数は、このような用途を想定して設計されています。
`preproc` を使うと、Carp コンパイラの通常の C コード出力よりも前に、任意の C コードを挿入できます。`preproc` に渡したコードは、ファイルのインクルード (`includes`) の後、ほかのすべての C コードが出力される前に出力されます。

`preproc` は `C` 型の値を引数に取るため、`Unsafe.emit-c` と組み合わせる必要があります。`preproc` に渡した C コードは一切検査されないので、注意してください。

`preproc` で C のシンボルを定義した場合でも、Carp のコードから参照するには `register` を呼び出す必要があります。例えば、次のコードでは、`preproc` を使って C のマクロと関数を Carp コンパイラの出力内で利用できるようにし、それらのシンボルを Carp ソースの `main` 関数から参照できるように `register` を呼び出しています。

```
(Unsafe.preproc (Unsafe.emit-c "#define FOO 0"))
(Unsafe.preproc (Unsafe.emit-c "void foo() { printf(\"%d\\n\", 1); }"))

(register FOO Int)
(register foo (Fn [] ()))

(defn main []
  (do (foo)
      (IO.println &(fmt "%d" FOO))))
```

この方法で、コンパイラの出力内で参照する必要がある仮の定義を追加できます。補助関数、マクロ、プリプロセッサディレクティブが長い、または複雑な場合は、別の `h` ファイルで定義し、Carp のソースから `relative-include` で取り込む方がよいでしょう。

### 型の登録 (Registering Types)

Carp には、C で定義された型を登録する方法がいくつかあります。型の登録には `register-type` 関数を使えます。シンボルだけを引数にして `register-type` を呼び出すと、そのシンボルに対応する名前の C の型が登録されます。例えば、次のコードは C の型 `A` を Carp の型 `A` として登録します。

```c
typedef int A;
```

```clojure
(register-type A)
```

このように `register-type` を呼び出すと、Carp のコードで型名を使える場所ならどこでも、型 `A` を使えるようになります。例えば、関数の型シグネチャで使えます。

```clojure
(sig a-prn (Fn [A] String))
```

この型の登録で Carp に登録されるのは、型名 *だけ* です。つまり、Carp のプログラムから見ると、この型は完全に「不透明」です。Carp は型が存在することは知っていますが、その実装や、その型の値を構築する方法は知りません。それらはすべて C のコードに任されています。

Carp のコードからこの型の値を構築したい場合は、次の 2 つの方法があります。

1. C で型の初期化関数 (initializer) を自分で定義し、Carp に登録します。
2. `register-type` を使って、Carp 側で型の初期化関数を生成します。

C で型の初期化関数を定義した場合は、`register` を使うと Carp から呼び出せます。

```c
typedef int A;

A initializer() {
  return 0;
}
```

```clojure
(register-type A)
(register initializer (Fn [] A))
;; A 型の値を返す
(initializer)
```

もう 1 つの方法は、`register-type` の呼び出しに型のメンバーを指定した空でない配列を追加し、外部の型の初期化関数、getter、setter、表示用の関数を Carp に生成させることです。Carp が生成する初期化関数は、指定したフィールドだけを初期化します。フィールドを省略したり、名前を誤ったりすると、生成された初期化関数がエラーを引き起こす可能性があります。

```clojure
(register-type B [])
:i B
=> B : Type
     init : (Fn [] B)
     prn  : (Fn [(Ref B q)] String)
     str  : (Fn [(Ref B q)] String)
}
(register-type C [x Int])
:i C
=> C : Type
   C : Module {
     init     : (Fn [Int] C)
     prn      : (Fn [(Ref C q) String])
     str      : (Fn [(Ref C q) String])
     set-x    : (Fn [C, Int] C)
     set-x!   : (Fn [(Ref C q), Int] ())
     update-x : (Fn [C, (Ref (Fn [Int] Int) q)] C)
     x        : (Fn [(Ref C q)] (Ref Int q))
}
```

> 訳注: 原文の出力例では、`C` の `prn` と `str` の型シグネチャで、返り値に当たる `String` が引数配列の中に置かれています。直前の `B` の例と型シグネチャの形式から、`(Fn [(Ref C q)] String)` を意図していると考えられます。出力例は原文のままです。

その型の `prn` 関数と `str` 関数は、対応するインターフェースも自動的に実装します。

*Carp は、既定では外部の型に関連付けられたメモリを管理しない* ことに注意してください。Carp で定義した型とは異なり、登録した型に対して `copy` 関数と `delete` 関数は生成されません。便宜上、登録した型に対して生成された初期化関数を使っている場合でも、その型の値に関連付けられたメモリは手動で管理する必要があります。登録した型のメモリを Carp に管理させたい場合は、`copy` インターフェースと `delete` インターフェースの実装を用意できます。

必要に応じて、文字列の引数を追加して、登録した型に対して Carp が出力する名前を上書きできます。これは、C 側の型名が Lisp や Carp の命名規則に従っていない場合に便利です。例えば、C の型名は小文字で始まることがありますが、Carp ではすべての型名を大文字で始める必要があります。

```clojure
;; C コードでは "A" として出力される
(register-type A)
;; C コードでは "a_type" として出力される
(register-type A "a_type")
;; C コードでは "b_type" として出力される
(register-type B "b_type" [x Int])
```

## コールバック (Callbacks)

C の API の中には、コールバックを使うものがあります。例として、コールバックと引数を受け取り、その関数を呼び出した結果を返す C 関数を定義してみます。

```clojure
(deftemplate runner (Fn [(Ptr ()) (Ptr ())] a)
                    "$a $NAME(void* fnptr, void* args)"
                    "$DECL {
                       return (($a(*)(void*))fnptr)(args);
                    }")

; 環境の変数をキャプチャするラムダ (lambda) を使う
(let [x 20 y 22 fnfn (fn [] (+ @&x @&y))]
  (= (runner (Function.unsafe-ptr &fnfn) (Function.unsafe-env-ptr &fnfn))
     42))

; 静的関数を使う
(defn double [x] (Int.* @x 2))

(let [x 42]
  (= (runner (Function.unsafe-ptr &double) (Unsafe.coerce &x))
     84))
```

最初の例では、変数をキャプチャするラムダを使います。`Function.unsafe-ptr` で関数への `void*` を取得できます。環境をキャプチャするラムダの場合、その関数の第 1 引数は環境なので、`Function.unsafe-env-ptr` を使ってその環境を渡す必要があります。

2 番目の例では静的関数を使うので、ここでも `Function.unsafe-ptr` を使えます。渡す引数は、`Ref` から `(Ptr ())` へ強制変換する必要があります。

すべてが void ポインタに変換されるため、型安全性はすべて失われます。その操作が安全であることを保証する責任は呼び出し側にあります。また、`Ptr` のライフタイムと、それが表す関数や環境のライフタイムとの関係も重要です。原文では、この関係を「doesn't not exceed (超えないわけではない)」と記述しています。

> 訳注: 原文は二重否定になっています。ポインタの安全性について述べている文脈から、`Ptr` のライフタイムが、それが指す関数や環境のライフタイムを「超えない」ことを確認する、という意味と考えられます。

## Headerparse

`headerparse` は、C のヘッダーを解析して `register` と `register-type` を生成し、C のバインディング作成を支援する Haskell スクリプトです。原文では Carp のソースリポジトリの `./headersparse` フォルダーにあると説明されています。次のように使えます。

> 訳注: 原文のフォルダー名は `./headersparse` ですが、直後のコマンドと固定版リポジトリのディレクトリ名は `./headerparse` です。

```sh
stack runhaskell ./headerparse/Main.hs -- ../path/to/c/header.h
```

スクリプトは次のフラグを受け付けます。

- `[-p|--prefixtoremove thePrefix]`: C の識別子から接頭辞を取り除きます。
- `[-f|--kebabcase]`: 識別子をケバブケース (kebab-case) に変換します。
- `[-c|--emitcname]`: バインディングの後に C の識別子名を常に出力します。

### 例 (Example)

次の C ヘッダーに対してスクリプトを実行すると、

```sh
stack runhaskell ./headerparse/Main.hs -- -p "MyModule_" -f ../path/to/aheader.h
```

```c
// aheader.h
bool MyModule_runThisFile(const char *file);
```

次の内容が出力されます。

```clojure
(register run-this-file (λ [(Ptr CChar)] Bool) "MyModule_runThisFile")
```

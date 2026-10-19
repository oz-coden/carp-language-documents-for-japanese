# Carp

原文: [LanguageGuide.md(英語)](https://github.com/carp-lang/Carp/blob/9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5/docs/LanguageGuide.md)

翻訳元のコミットは `9f6fa9c11989eadc272ec8b10eab6eb873ae0aa5` です。
この文書は英語原文を日本語に翻訳・編集した非公式の文書です。内容の完全性・正確性は保証しません。
原文のコード例や仕様説明を独自に修正せず、必要な箇所には訳注を付けています。
翻訳方針は [TRANSLATION.md](TRANSLATION.md)、採用語は [GLOSSARY.md](GLOSSARY.md) を参照してください。

## 言語ガイド (The Language)

### 導入 (Introduction)

Carp は見た目こそ Clojure に似ていますが、実行時の意味論 (runtime semantics) は ML や Rust のものに非常に近いです。
型は型推論によって自動的に決まりますが、読みやすさのために `the` キーワードで型注釈を付けることができます (後述)。

メモリ管理は静的解析によって行われ、その値はそれが生成された関数によって所有されます。
値が返されたり、別の関数に渡したりしたとき、その元の関数はその値の所有権を放棄します。
その後、元の関数でその値を使用しようとすると、コンパイルエラーが発生します。
値を別の関数に一時的に貸し出す (借用させる) には (例えば、表示するためなど)、`ref` 特殊形式 (または `&` リーダーマクロ) を使用して参照を作成する必要があります。

詳しくは [メモリ管理の詳細](Memory-JP.md) を参照してください。

### コメント (Comments)

```clojure
;; コメントはセミコロンから始まり、行末まで続く
```


### データリテラル (Data Literals)

```clojure
100     ;; Int
1500l   ;; Long
3.14f   ;; Float
10.0    ;; Double
1b      ;; Byte
true    ;; Bool
"hello" ;; &String
#"hello" ;; &Pattern
\e      ;; Char
[1 2 3] ;; (Array Int)
{1 1.0 2 2.0} ;; (Map Int Double)
```

### 型リテラル (Type Literals)

```clojure
t ;; 型変数は小文字で始まる
(f t) ;; 型コンストラクタ変数 (type constructor variable)。`(Maybe Int)` には一致するが、`Int` には一致しない
Int
Long
Float
Double
Byte
Bool
String
Pattern
Char
(Array t)
(Map <key-type> <value-type>)
(Fn [<arg-type1> <arg-type2> ...] <return-type>) ;; 関数型
```

### 動的コードでのみ使用できるデータリテラル (Dynamic-only Data Literals)

現時点では、以下のデータ型はコンパイルされないコード内でのみ扱えます。

```clojure
(1 2 3) ; リスト
foo ; シンボル
```

### 定義 (Defining things)

```clojure
(defn function-name [<arg1> <arg2> ...] <body>) ;; 関数を定義する (コンパイルされ、REPL では呼び出せない)
(definterface interface-name (Fn [<t1> <t2>] <return>)) ;; 複数の実装を持てるジェネリック関数 (generic function) を定義する
(def variable-name value) ;; グローバル変数を定義する (現時点では、プリミティブ型の定数のみを扱う)
(defmacro <name> [<arg1> <arg2> ...] <macro-body>) ;; 呼び出し時に実引数が評価されないマクロを定義する
(defdynamic <name> <value>) ;; REPL か、コンパイル時のみ使用できる変数を定義する
(defndynamic <name> [<arg1> <arg2> ...] <function-body>) ;; REPL か、コンパイル時のみ使用できる関数を定義する
(defmodule <name> <definition1> <definition2> ...) ;; プログラムを分割して整理するための主な方法
```

トップレベルの `defn` および `def` 形式は、ファイル内での定義順序に関係なく互いに参照し合うことができます。
つまり、関数が定義される前にそれを呼び出すことが可能であり、相互再帰関数も特別な宣言なしに動作します：

```clojure
(defn main [] (IO.println &(Int.str (add-one 41))))
(defn add-one [x] (+ x 1))

;; 相互再帰
(defn is-even [n] (if (= n 0) true (is-odd (- n 1))))
(defn is-odd [n] (if (= n 0) false (is-even (- n 1))))
```

定義順序の独立性は、単一のファイル内の `defn` および `def` 形式にのみ適用される点に注意してください。
`defmodule`、`use`、`sig`、およびマクロなどの他の形式は、依然として記述された順序で処理されます。
`(load ...)` を通じて読み込まれたファイルも、読み込まれた順序で処理されます。

末尾位置にある自己再帰関数は自動的にループに最適化され、深い再帰によるスタックオーバーフローを回避します。
これは、`String` などのメモリ管理の対象となる型 (managed type) がスコープ内にある場合でも機能します。

```clojure
(defn sum-to [n acc]
  (if (= n 0) acc (sum-to (- n 1) (+ acc n))))

(defn repeat-str [n acc]
  (if (= n 0)
    acc
    (let [piece @"x"]
      (repeat-str (- n 1) (StringCopy.append &acc &piece)))))
```

末尾位置は、`if`、`do`、`let`、および `the` 形式を通じて認識されます。
いずれかの仮引数が参照型である場合、この最適化は適用されません。

相互再帰関数のグループについても、
仮引数の型、仮引数の名前、および戻り値の型が共通している場合は最適化されます：

```clojure
(defn is-even [n]
  (if (= n 0) true (is-odd (- n 1))))

(defn is-odd [n]
  (if (= n 0) false (is-even (- n 1))))
```

### `cond` を使った条件分岐 (Conditional statements with `cond`)

`cond` 文は、指定された条件が真の場合にコードブロックを実行します。条件が偽の場合は、別のコードブロックを実行することができます。

```clojure
(doc cond "これはcondのドキュメントです")
```

使用例：

```clojure
(cond
          (<condition_1>) (<code_1>) ;; code_1 が実行されるのは、condition_1 が真のとき
          (<condition_2>) (<code_2>) ;; code_2 が実行されるのは、condition_2 が真のとき
          (<code_3>) ;; code_3 が実行されるのは、condition_1 と condition_2 のどちらも偽のとき
```

> 訳注: 上の一般形は、末尾の `(<code_3>)` の後に外側の `cond` を閉じる `)` が必要だと考えられます。原文どおりの例を掲載しています。

これは、10 より小さいか大きいかに応じてメッセージを出力する例です。

```clojure
(cond
  (< 10 1) (println "実行されない！")
  (> 10 1) (println msg)
  (println "実行されない！"))
```

> 訳注: 上の例の `msg` は原文中で定義されていません。文脈上、出力したいメッセージを表す値と考えられます。

### 特殊形式 (Special Forms)

以下の形式は Carp のソースコードで使用でき、型チェックやその他の静的解析を経たのちに C 言語にコンパイルされます。
そのうち最初の 3 つは、動的関数でも利用可能です。

```clojure
(fn [<arg1> <arg2> ...] <body>) ;; ラムダ関数 (lambda) を作る。クロージャ (closure) とも呼ぶ
(let [<var1> <expr1> <var2> <expr2> ...] <body>) ;; 局所的な束縛 (binding) を作る
(do <expr1> <expr2> ... <return-expression>) ;; 副作用のある関数を実行し、その後で値を返す
(if <expression> <true-branch> <false-branch>) ;; 分岐
(while <expression> <body>) ;; 式が偽になるまでループする
(use <module>) ;; <module> にあるシンボルをすべてスコープの中に取り込む
(with <module> <expr1> <expr2> ...) ;; 局所スコープの `use`。このスコープ内のすべての式は <module> 内のシンボルを参照できる
(match <expression> <case1> <expr1> <case2> <expr2> ...) ;; <expression> を直和型 (sumtype) のコンストラクタの集合に対してパターンマッチングする
(match-ref <expression> <case1> <expr1> <case2> <expr2> ...) ;; 参照型の <expression> に対してパターンマッチングを行い、そのメンバーの所有権を取得しない
(ref <expression>) ;; 所有されている値を借用する
(set! <variable> <expression>) ;; 変数を変更する
(the <type> <expression>) ;; 式の型を明示的に宣言する
```

これは、`the` 形式を使用して、整数のみを受け入れる恒等関数を作成する例です：

```clojure
(defn f [x]
  (the Int x))
```

### リーダーマクロ (Reader Macros)

```clojure
&x ;; (ref x) と同じ
@x ;; (copy x) と同じ
```

### 名前付きホール (Named Holes)

Carp のような静的型付け言語を使用する場合、プログラムの特定の箇所でどの値を使用すべきか判断することが難しいときがあります。
そのような場合、ホール (hole) という概念が役立ちます。
ソースコードにホールを追加し、リロード (`:r`) するだけで、Carp のコンパイラがその箇所にどの型が当てはまるかを判断してくれます。

```clojure
(String.append ?w00t "!") ;; 型エラーが発生し、`?w00t` の型が `&String` であることがわかる
```

### 動的コードの評価中の特殊形式 (Special forms during evaluation of dynamic code)

```clojure
(quote <expression>) ;; 式のそれ以上の評価を避ける
(and) (or) (not) ;; 論理演算子
```

### 動的関数 (Dynamic functions)

これらは REPL およびマクロの評価中にのみ使用できます。
以下に、最もよく使われるもののいくつかを挙げます：

```clojure
(car <collection>) ;; リストまたは配列の最初の要素を返す
(cdr <collection>) ;; リストまたは配列の最初の要素を除くすべての要素を返す
(cons <expr> <list>) ;; <expr>の値を<list>の最初の要素として追加する
(cons-last <expr> <list>) ;; <expr>の値を<list>の最後の要素として追加する
(list <expr1> <expr2> ...) ;; 一連の評価済みの式からリストを作成する
(array <expr1> <expr2> ...) ;; 一連の評価済みの式から配列を作成する
```

`Dynamic` モジュールで利用可能なすべての関数を確認するには、REPL で `(info Dynamic)` と入力してください。

### 構造体 (Structs)

Carp で定義された構造体型には、新しいインスタンスを作成するために使用できる `init` メソッドがあります。
このメソッドは、定義された順序ですべての実引数を指定して呼び出す必要があります。

```clojure
(deftype Vector2 [x Int, y Int])

(let [my-pos (Vector2.init 10 20)]
  ...)

;; 各メンバーに対してレンズ (lens) が自動生成される。参考として、型シグネチャを以下に示す
;; Vector2.x (Fn [(Ref Vector2)] (Ref Int))
(Vector2.x &my-pos) ;; => 10
;; Vector2.set-x (Fn [Vector2 Int] Vector2)
(Vector2.set-x my-pos 30) ;; => (Vector2 30 20)
;; Vector2.set-x! (Fn [(Ref Vector2), Int] ())
(Vector2.set-x! &my-pos 30) ;; => ベクトル my-pos をその場で更新し、() を返す
;; 型シグネチャ内の、関数への参照 `(Ref (Fn [Int] Int))` に注意
;; Vector2.update-x (Fn [Vector2, (Ref (Fn [Int] Int))] Vector2)
(Vector2.update-x my-pos inc) ;; => (Vector2 11 20)
;; ここにはラムダ関数も渡せる
(Vector2.update-x my-pos &(fn [n] (* n 3))) ;; => (Vector2 30 20)
```

### 直和型 (Sumtypes)

直和型を定義するには、2 つの方法があります。

**列挙型 (Enumeration)**

```clojure
(deftype MyEnum
  Kind1
  Kind2
  Kind3)
```

**データを持つ場合 (Data)**

```clojure
(deftype (Either a b)
  (Left [a])
  (Right [b]))
```

バリアント (variant) は、呼び出し式と同じ構文で作成できます。

```clojure
(MyEnum.Kind1)
(Either.Left 10)
(Either.Right 11)

;; または `use` 文を使用する
(use Either)
(Left 10)
(Right 11)

(use MyEnum)
(Kind1)
(Kind2)
(Kind3)
```

パターンマッチングを使用すると、安全に値を抽出できます：

```clojure
(defn get [either]
  (match either
    (Either.Left a) a
    (Either.Right b) b))

(with MyEnum
  ;; 一般的な「それ以外」の分岐も指定できる
  (match myenum
    (Kind1) (logic1)
    _ (logic-other)))
```

なお、`match` は *値* (参照ではなく) に対して動作し、パターンマッチングの対象となる値の所有権を取得します。参照に対してパターンマッチングを行う場合は、`match-ref` を使用できます。

```clojure
(match-ref &might-be-a-string
  (Just s) (IO.println s)
  Nothing (IO.println "Got nothing"))
```

このコードでは、`might-be-a-string` の所有権を取得しない点に注意してください。
また、最初のケースの `s` は参照です。この状況では、`Maybe` を値に分解することは安全ではないためです。

**注:** 直和型は、128 個を超える要素 (コンストラクタとも呼ばれる) を持つことはできません。これをバイトに由来する制限だと感じるなら、その認識は正しいです。これは制限ではありますが、原文の記述時点では問題となっていません。

### 再帰型 (Recursive Types)

Carp は、再帰が間接参照 (つまり `Box` や `Ptr`) を経由する場合に限り、再帰型をサポートしています。
直接的な再帰は、コンパイラが各型の具体的な有限サイズを計算できなければならないため、許可されません。

例 (許可されるもの)：

```clojure
;; 直和型を使用した連結リスト
(deftype (List a)
  (Nil)
  (Cons [a (Box (List a))]))

;; 再帰的な構造体
(deftype Node [value Int next (Box Node)])
```

直接再帰 (許可されない)：

```clojure
(deftype Bad [self Bad])
```

`Box` はメモリ管理の対象となる線形ポインタ型であるため、所有権のルールが適用されます。
`Ptr` はメモリ管理の対象外 (unmanaged) であり、ライフタイムや解放を自身で処理する高度なユースケース向けです。

### モジュールと名前解決 (Modules and Name Lookup)

関数や変数は、名前が付けられ、ネスト可能なモジュール内に格納することができます。
モジュール内のシンボルを使用するには、次のようにモジュール名で修飾する必要があります：`Float.cos`。

モジュールを*使用*することで、修飾せずにそのメンバーにアクセスできるようになります：

```clojure
(use Float)

(defn f []
  (cos 3.2f))
```

同じ名前のシンボルを含む複数のモジュールが使用されている場合、型推論器は (コード内の型に基づいて) どのシンボルを指しているのかを判別しようとします。
判別できない場合は、エラーが表示されます。
例えば、モジュール `String` と `Array` の両方に `length` という名前の関数が含まれています。
次のコードでは、`Array` 用の関数が必要であり、実際にその関数が呼び出されることがわかります：

```clojure
(use String)
(use Array)

(defn f []
  (length [1 2 3 4 5]))
```

次の例では、どの型が意図されているのか判別できません：

```clojure
(use String)
(use Array)

(defn f [x]
  (length x))
```

型を指定することで、このエラーは解決されます：

```clojure
(use String)
(use Array)

(defn f [x]
  (String.length x))
```

> 訳注: 原文は上の例を「型を指定する」と説明しています。例のコードでは `String.length` とモジュール名で修飾して、呼び出す関数を明示しています。

モジュールを `use` すると、その宣言が現在のスコープに取り込まれます。
グローバルスコープでモジュールを `use` すると、`use` の呼び出し後にその宣言のすべてがグローバルスコープに取り込まれます。
同様に、別のモジュールのスコープ内でモジュールを `use` すると、そのモジュールのスコープ内では修飾子なしでその宣言を参照できます：

```clojure
(use String)

;; グローバルスコープで `use` しているのは `String` モジュールだけなので、
;; `length` をモジュール名で修飾せずに参照できる
(defn f [x]
  (length x))

(defmodule Foo
  (use Array)
  ;; グローバルスコープでは `String` モジュールが使用されており、
  ;; `Foo` モジュールでは `Array` も `use` しているため、参照先を明確にするには、
  ;; `length` の呼び出しに再びモジュール修飾子が必要になる
  (defn g [xs]
    (Array.length xs)))
```

場合によっては、モジュールの宣言を限られた数の式に対してのみスコープ内に取り込む方が便利なことがあります。
これは `with` 形式を使用して行うことができます：

```clojure
(defmodule Foo
  ;; ここではモジュール修飾子を使用する必要がある
  ;; `Foo` モジュールのスコープ内で `use` を呼び出していないため
  (defn f [x]
    (String.length x))
  ;; `with` 形式を使用すると、そのモジュールの宣言を
  ;; `with` のスコープ内のすべての式から修飾子なしで参照できる
  (with String
    (defn g [x]
      (length x))))
```

一部の束縛をモジュール内部に限定しておくことが有用な場合があります。
そのために `private` や `hidden` を使用できます：

```clojure
(defmodule Say
  ;; `Say` モジュール外から `hell` にアクセスできないようにする
  (private hell)
  ;; `Say` 内の束縛一覧に `hell` が表示されないようにする
  (hidden hell)
  (defn hell [] @"hell")

  ;; `private` および `hidden` は `def` と `defn` で使用できる
  (private o)
  (hidden o)
  (def o @"o")

  ;; モジュール内では `hell` と `o` にアクセスできる
  (defn hello [] (String.concat &[(hell) @&o])))


;; `hello` は private ではないため、有効な呼び出し
(Say.hello)

;; `hell` は `Say` モジュール内で private なので、コンパイル時にエラーになる
(Say.hell)
```

`defn-` および `def-` は、束縛を定義し、それを `private` および `hidden` としてマークするための省略形として使用できます。
以下の例は、前の例と同等です：

```clojure
(defmodule Say
 (defn- hell [] @"hell")
 (def- o @"o")
 (defn hello [] (String.concat &[(hell) @&o])))
```

### インターフェース (Interfaces)

インターフェースは、複数の具体的な関数が実装できるジェネリック関数の型シグネチャを指定します。
`definterface` を使用して、関数の名前と型シグネチャを渡すことで、インターフェースを定義できます：

```clojure
(definterface speak (Fn [a] String))
```

`implements` を使用すると、関数をインターフェースの実装として宣言できます。
例えば、次のコードでは `Dog.bark` および `Cat.meow` を `speak` の実装として宣言しています：

```clojure
(definterface speak (Fn [a] String))

(defmodule Dog
  (defn bark [aggressive?]
    (if aggressive? @"WOOF!" @"woof!"))
  (implements speak Dog.bark))

(defmodule Cat
  (defn meow [times] (String.repeat times "meow!"))
  (implements speak Cat.meow))
```

インターフェースの型シグネチャを満たす関数のみが、そのインターフェースを実装できます。
例えば、以下の関数は実引数の数が間違っており、戻り値の型も `speak` の戻り値の型と一致しないため、`speak` の有効な実装ではありません：

```clojure
(defmodule Number
  ;; 数字が話せるなんて、誰が思っただろう？
  (defn holler [] "WOO!")
  (implements speak Number.holler))
=> [INTERFACE ERROR] Number.holler : (Fn [] (Ref String a)) doesn't match the interface signature (Fn [a] String)
```

インターフェースを名前で呼び出す際、Carp は現在のコンテキストと各実装の型シグネチャを用いて、
型チェックに合格する実装を呼び出します：

```clojure
(speak 2) ;; Int -> String, Cat.meow
=> "meow!meow!"
(speak false) ;; Bool -> String, Dog.bark
=> "woof!"
```

特定のコンテキストにおいて、複数のインターフェース実装が Carp の型チェッカーの要件を満たす場合、Carp は曖昧性を示すエラーを出します。

```clojure
(defmodule Pikachu
  (defn pika [times] (String.repeat times "pika!"))
  (implements speak Pikachu.pika))

(speak 2) ;; Int -> String, Cat.meow OR Pikachu.pika
=> There are several exact matches for the interface `speak` of type `(Fn [Int] String)` at line 1, column 2 in 'REPL'
Possibilities:
    Cat.meow : (Fn [Int] String)
    Pikachu.pika : (Fn [Int] String) at REPL:1:1.
```

このような場合、必要な実装関数を直接呼び出すことで、Carp コンパイラが呼び出しの曖昧性を解消できるよう手助けする必要があります。
通常、同じ型シグネチャを持つ複数の実装を提供することはあまり意味がありません。

### C との相互運用 (C Interop)

```clojure
(system-include "math.h") ;; コンパイル時に #include <math.h> となる
(relative-include "math.h") ;; コンパイル時に #include "$carp_file_dir/math.h" となる。carp_file_dir は呼び出し元の .carp ファイルを含むフォルダの絶対パスである

(register blah (Fn [Int Int] String)) ;; 2 つの Int を受け取り、String を返す関数 "blah" を登録する
(register pi Double) ;; Double 型のグローバル変数 "pi" を登録する

(register blah (Fn [Int Int] String) "exit") ;; 関数 "blah" を登録するが、生成される C コードでは "exit" という名前を使用する

(register-type Apple) ;; 不透明な C 型を登録する
(register-type Banana [price Double, size Int]) ;; 外部の C 構造体を登録する。これにより getter、setter、updater が生成される
```

C 言語の型名は小文字 (例えば `size_t`) であることが多く、単にそれらを登録するだけでは問題が生じます。
Carp は、そのような変数をジェネリック型とみなしてしまうためです。
このような型と相互運用できるようにするため、`register-type` は型名の後にオプションの文字列を受け取ります。例は以下の通りです：

```clojure
(register-type SizeT "size_t")
```

これにより、Carp コード内の型名は `SizeT` となり、生成される C コードでは代わりに `size_t` が使用されます。

C との相互運用の詳細は [C との相互運用](CInterop-JP.md) を参照してください。

### パターン (Patterns)

パターンは正規表現と似ていますが、同じものではありません。
これは [Lua(英語)](http://lua-users.org/wiki/PatternsTutorial) から派生したもので、
文字列の中から何かを見つけたり、文字列から何かを抽出したりしたい場合に役立ちます。

パターンには選択 (alternation) がないため、正規表現よりもシンプルです。
とはいえ、非常に有用な場合が多く、単純であるため、処理も高速で、動作も予測しやすいという利点があります。

以下に、API の概要を簡単に紹介します：

```clojure
;; パターンはリテラルで初期化することも、文字列から作成することもできる
#"[a-z]"
(Pattern.init "[a-z]")

;; パターンから文字列を取得することもできる
(str #"[a-z]")
(prn #"[a-z]")

;; 文字列内でパターンが一致する位置をインデックスとして取得できる
(Pattern.find #"[a-z]" "1234a") ; => 4
(Pattern.find #"[a-z]" "1234")  ; => -1

;; 一度に複数の一致箇所も検索できる！
(Pattern.find-all #"[a-z]" "1234a b") ; => [4 6]


;; matches? は、文字列がパターンに一致するかどうかを確認する
(Pattern.matches? #"(\d+) (\d+)" "  12 13") ; => true

;; match-groups は、最初の一致に含まれるすべてのマッチグループを返す
(Pattern.match-groups #"(\d+) (\d+)" "  12 13") ; => ["12" "13"]

;; match-str は、最初の一致に対応する文字列全体を返す
(Pattern.match-str #"(\d+) (\d+)" "  12 13") ; => "12 13"

;; global-match は、すべての一致に含まれるマッチグループをすべて取得する
(Pattern.global-match #"(\d+) (\d+)" "  12 13 14 15") ; => [["12" "13"] ["14" "15"]]

;; substitute を使用すると、文字列内のパターンを n 回置き換えられる
(Pattern.substitute #"sub-me" "sub-me sub-me sub-me" "replaced" 1) ; => "replaced sub-me sub-me"

;; すべての出現箇所を置き換える場合は、-1 を使用する
(Pattern.substitute #"sub-me" "sub-me sub-me sub-me" "replaced" -1) ; => "replaced replaced replaced"
```

#### パターンの制限 (Limitations of Patterns)

前述の通り、パターンは正規表現ほど表現力が豊かではありません。
その根本的な違いは、パターンにはバックトラック機能がないことです。
つまり、パターンでは選択 (分岐した地点に戻ることができないため) を表現できず、
また、左側の非貪欲なマッチを縮小することもできません。
後者の点は直感的に分かりにくいかもしれませんので、例を見てみましょう：

```
(Pattern.match-all-groups #"1.-2" "1 1 2") ; => [[@"1 1 2"]]
```

有効な、より非貪欲 (短い) な一致は `"1 2"` であったはずですが、一致のサイズを縮小するために
照合を開始した後に左側へ戻る必要があったため、これは行われません。
このように、`-` は正規表現の `*?` と似ていますが、同じものではありません。
多くの場合、問題を解決できる、より明示的なパターンのバリエーションを見つけることができます
(上記の場合、例えば `#"1\s-2"` が望ましかったかもしれません)。

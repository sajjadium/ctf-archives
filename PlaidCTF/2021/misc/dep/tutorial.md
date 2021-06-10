# `dep` Tutorial

`dep` is an implementation of something similar to the [Calculus of Constructions](https://en.wikipedia.org/wiki/Calculus_of_constructions). It is different in a some ways, so this tutorial describes its usage by implementing a few examples. All blocks of code in the tutorial can be run in the interpreter one after another to see the results!

Each valid expression in the language has a type. The fact that an expression `e` has type `t` is denoted by `e : t`.

The first useful construct to be aware of is called a _universe_ or a _sort_. It is denoted by `#`. Some example universes are `#0` and `#3`. Each universe is of the type of the next universe. Thus, `#0 : #1`, `#1 : #2`, etc. Since speaking in terms of numbered universes is cumbersome, we'll just name the first two:
```
Prop = #0
Type = #1
```

If you run the above in the interpreter, it will add it into its environment and also tell you the types of each. It is useful to run things in the interpreter to see if the expression is valid, and to check its type. The interpreter is smart enough to simplify things and try to give you a nice looking output, as we'll see when we proceed.

The next construct is the notion of _abstraction_. It is how you define new functions. If you're used to lambda functions in languages, this is exactly the same. Something like `(x:t)->e` denotes a new abstraction which takes in an argument `x` of type `t` and returns `e` (which may contain usages of `x` in it). Using this, we can define the simplest function that exists in our language, the identity function on `Prop`s:
```
(x:Prop)->x
```

When you run this in the interpreter, you'll receive the result `((x : Prop) -> x) : (x : Prop) => Prop`. This means that it was able to see that it has the type `(x : Prop) => Prop`. Notice that the arrow `->` has changed to an `=>`. This is the next construct in the language. This is called the _Pi_. It is what makes this particular language much more powerful in its types. The core syntax for Pi looks very similar to abstraction: `(x:t)=>e`. However, it behaves quite differently: it acts effectively an abstraction at the type level, which makes it quite interesting, since it allows types to _depend_ upon values. Try checking the type of:
```
(x:Prop) => Prop
```

Such a Pi abstraction is a core feature of [Dependent Types](https://en.wikipedia.org/wiki/Dependent_type), which can be used to prove the absence of bugs in real programs! There is a famous strong correspondence between proofs of theorems and type checking called the [Curry-Howard isomorphism](https://en.wikipedia.org/wiki/Curry%E2%80%93Howard_correspondence). We won't dive into this too much though.

BTW, we can already use the current set of things we know to define ourselves some basic useful types and values. In particular, let's go ahead and define the booleans:
```
Bool = (a:Type) => (t:a) => (f:a) => a
true = (a:Type) -> (t:a) -> (f:a) -> t
false = (a:Type) -> (t:a) -> (f:a) -> f
```

While they don't seem terribly useful just yet, they are a big milestone in the language. Suddenly, without the language knowing about booleans before, they can now tell that `true` and `false` are of type `Bool`. An interesting challenge, left to the reader, is to show that these two are the only inhabitants of the `Bool` type.

To make these useful, we need to introduce the last construct in the language: _application_. Function application is used to pass arguments into an abstraction. The syntax used is `(f x)` to mean passing `x` into the function `f`. The language supports multiple arguments to functions by [Currying](https://en.wikipedia.org/wiki/Currying), thus you can also write applications like `(g x y z)` if the function `g` took 3 arguments.

With this, we can make the booleans useful, by defining the standard operations on them:
```
and = (x:Bool) -> (y:Bool) -> (x Bool y false)
or = (x:Bool) -> (y:Bool) -> (x Bool true y)
not = (x:Bool) -> (x Bool false true)
```

We leave it as an exercise to the reader to understand why each of these operations work. We recommend starting from `not` to understand them well. You can also try testing these out, to see if they give the right results:
```
(not false)
(and true (or false (not false)))
```

Notice how the interpreter is able to perform these simplifications and give us a very nice and convenient result in the form of things we've defined before. The interpreter internally performs all the computation and then tries to pretty-print it using things you've defined. This is what allows for the very succinct results that it is able to show. Note that the interpreter has no internal notion of what a boolean is, or what `and`/`or`/`true`/etc. are. To test this out, spin up a new session and name things differently, and see how it works. Maybe instead of `Bool`, `true` and `false`, you like the names `dog`, `goodboy` and `goodgirl`. Go nuts!

Back to expanding upon what we've defined: given this core set of language features, we can now start building more advanced things. We can define a convenient syntax for if-then-else (although directly using the booleans also works):
```
ite = (a:Type) -> (cond:Bool) -> (ifTrue:a) -> (ifFalse:a) -> (cond a ifTrue ifFalse)
```

Next up, we want to define the natural numbers, because a programming language without numbers is fairly useless. We do this by defining the type `Nat` and a member `0` of it, as well as a successor function `succ`:
```
Nat = (a:Type) => (s:(_:a)=>a) => (z:a) => a
0 = (a:Type) -> (f:(_:a)=>a) -> (x:a) -> (x)
succ = (n:Nat) -> (a:Type) -> (f:(_:a)=>a) -> (x:a) -> ((n a f) (f x))
```

Suddenly with this, we can define a few small numbers:
```
1 = (succ 0)
2 = (succ 1)
3 = (succ 2)
4 = (succ 3)
5 = (succ 4)
6 = (succ 5)
7 = (succ 6)
8 = (succ 7)
9 = (succ 8)
10 = (succ 9)
11 = (succ 10)
```

Of course, just knowing numbers is not enough, we also want to be able to know if it is zero or not:
```
isZero = (n:Nat) -> (n Bool ((_:Bool) -> false) true)
```

Or maybe add them together?
```
add = (m:Nat) -> (n:Nat) -> (n Nat succ m)
```

Feel free to test out adding numbers together:
```
(add 3 (add 4 1))
```

Defining the predecessor function is quite a bit more complicated though, unfortunately. We simply provide it below with no further explanation:
```
Box = (a:Type) -> (h : (_ : a) => a) => a
value = (a:Type) -> (v:a) -> (h:(_:a)=>a) -> (h v)
extract = (a:Type) -> (k:(h:(_:a)=>a)=>a) -> (k ((x:a)->x))
inc = (a:Type) -> (f:(_:a)=>a) -> (k:(Box a)) -> (value a (k f))
const = (a:Type) -> (x:a) -> (_:(_ : a) => a) -> x
pred = (n:Nat) -> (a:Type) -> (f:(_:a)=>a)->(x:a) -> (extract a (n (Box a) (inc a f) (const a x)))
```

Side note: one cool thing that you might have noticed above is the definition of `Box`. This is the first usage of a mix of both standard abstraction and the Pi abstraction in the same definition. We use this to create a _polymorphic_ type! For people who like C++ or Rust syntax, it has created something like a `Box<a>` type. You can place any type you like into it to get back a type that can be used as per usual! Isn't it surprising how many complex concepts in other languages can arise from such a simple core language? :)

Anyways, back to our core definitions. Since we now have the predecessor function `pred`, we can easily define subtraction `sub`, which can then be used to define the less-then-or-equal operator `leq`, which can then be used to define equality `eq`:
```
sub = (m:Nat) -> (n:Nat) -> (n Nat pred m)
leq = (m:Nat) -> (n:Nat) -> (isZero (sub m n))
eq = (m:Nat) -> (n:Nat) -> (and (leq m n) (leq n m))
```

As you can see, basically anything that involves arithmetic computations can be defined using this language. We can also quite easily define complex data structures, by using ideas similar to the `Box` we defined earlier.

See what you can build with this language now! Go wild!

Suggestions for next things to build:
- Multiplication
- Factorial
- Powering
- Division

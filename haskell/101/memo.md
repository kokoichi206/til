https://www.youtube.com/watch?v=Vgu82wiiZ90&list=PLe7Ei6viL6jGp1Rfu0dil1JH1SHk9bgDV

## Functional Programming

- Pure functions
  - mathematically
- Immutable data
- No/Less side-effects
- Declarative
  - Imperative
    - tell the program what to do
    - algorithms
- Easier to verify

## haskell

- Lazy vs Strict
  - separate definitions and evaluation
  - only evaluated when needed

## tutorial

https://www.youtube.com/watch?v=02_H3LjqMr8

``` sh
❯ ghci
GHCi, version 9.10.3: https://www.haskell.org/ghc/  :? for help

ghci> :l tut
[1 of 2] Compiling Main             ( tut.hs, interpreted )
Ok, one module loaded.
ghci> :r
[1 of 2] Compiling Main             ( tut.hs, interpreted ) [Source file changed]
Ok, one module reloaded.
ghci> maxInt
9223372036854775807
ghci> :r
[1 of 2] Compiling Main             ( tut.hs, interpreted ) [Source file changed]
Ok, one module reloaded.
ghci> sumOfNums
500500
ghci> :t sqrt
sqrt :: Floating a => a -> a

# 型の -> は右結合だけど、関数適用は左結合！
# 
ghci> :t (+)
(+) :: Num a => a -> a -> a
ghci> :t truncate
truncate :: (RealFrac a, Integral b) => a -> b
```

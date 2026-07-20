-- Comments
{-
Multiline 
Comments
-}
import Data.List
import System.IO

maxInt = maxBound :: Int
minInt = minBound :: Int

-- Double
bigFloat = 3.99999999 + 0.00000004

always5 :: Int
always5 = 5

sumOfNums = sum [1..1000]

addEx = 5 + 6
modEx = mod 5 4
-- infix operator form
modEx2 = 5 `mod` 4

num9 = 9 :: Int
sqrtOf9 = sqrt (fromIntegral num9)

trueAndFalse = True && False
trueOrFalse = True || False
notTrue = not(True)

primeNumbers = [3,5,7,11]
morePrimes = primeNumbers ++ [13,17,19,23,29]

favNums = 2 : 7 : 21 : []
multiList = [[3,5,7],[11,13,17]]

morePrimes2 = 2 : morePrimes
lenPrimes = length morePrimes2

secondPrime = morePrimes2 !! 1
lastPrime = last morePrimes2

first3Primes = take 3 morePrimes2

is7InList = 7 `elem` morePrimes2

newList = [2,3,5]

-- return 30
prodPrimes = product newList

zeroToTen = [0..10]
evenList = [2,4..20]

-- ghci> letterList
-- "ACEGIKMOQSUWY"
letterList = ['A','C'..'Z']

-- -- infinite list, but not created until needed
-- infinPow10 = [10,20..]

many2s = take 10 (repeat 2)
many3s = replicate 10 3

-- [ 出力する式 | 変数 <- 元のリスト, 条件 ]
{-
    x * 3              結果に入れる値
    x <- [1..10]       1〜10を順番にxへ取り出す
    mod x 2 == 0       xが偶数のときだけ残す
-}
listTimes3 = [x * 3 | x <- [1..10], mod x 2 == 0]

divisBy9N13 = [x | x <- [1..500], mod x 13 == 0, mod x 9 == 0]

listBiggerThan5 = filter (>5) morePrimes2

evensUpTo20 = takeWhile (<=20) [2,4..]

{-
    foldl =>
    (((1 * 2) * 3) * 4) * 5
-}
multiOfList = foldl (*) 1 [2,3,4,5]



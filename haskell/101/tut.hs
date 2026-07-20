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

pow3List = [3^n | n <- [1..10]]

multiTable = [[x * y | y <- [1..10]] | x <- [1..10]]

randTuple = (1, "Random Tuple")
bobSmith = ("Bob Smith", 52)

bobsName = fst bobSmith
bobsAge = snd bobSmith

names = ["Bob", "Mary", "Tom"]
addresses = ["123 Main", "234 North", "567 South"]

-- ghci> namesNAddress
-- [("Bob","123 Main"),("Mary","234 North"),("Tom","567 South")]
namesNAddress = zip names addresses

-- ghci> :t zip
-- zip :: [a] -> [b] -> [(a, b)]
--
{-
    要素の長さは違ってもいい？
    => min(length a, length b) までの要素がペアになりそう。

    ghci> ab
    [(1,'a'),(2,'b'),(3,'c')]
-}
a = [1,2,3]
b = ['a','b','c','d','e','f']
ab = zip a b


main = do
    putStrLn "ur name?"
    name <- getLine
    putStrLn ("hi, " ++ name ++ ", how are you?")


addMe :: Int -> Int -> Int

-- funcName param1 param2 = operation (returned value)

-- ghci> :l tut
-- [1 of 2] Compiling Main             ( tut.hs, interpreted )
-- Ok, one module loaded.
-- ghci> :t addMe
-- addMe :: Int -> Int -> Int
addMe x y = x + y

sumMe x y = x + y

-- addTuples :: (Int, Int) -> (Int, Int) -> (Int, Int)

whatAge :: Int -> String
whatAge 16 = "You can drive"
whatAge 18 = "You can vote"
whatAge 21 = "You can drink"
whatAge x = "Nothing Important"
-- whatAge _ = "Nothing Important"


factorial :: Int -> Int
factorial 0 = 1
factorial n = n * factorial (n - 1)

-- 1 upto n
prodFact n = product [1..n]

isOdd :: Int -> Bool
isOdd n
    | n `mod` 2 == 0 = False
    | otherwise = True

isEven n = n `mod` 2 == 0 

whatGrade :: Int -> String
whatGrade age
    | (age >= 5) && (age <= 6) = "tttttt"
    | (age > 6) && (age <= 10) = "elementary"
    | (age > 10) && (age <= 15) = "middle"
    | (age > 15) && (age <= 18) = "high"
    | otherwise = "college?"

batAvgRating :: Double -> Double -> String
batAvgRating hits atBats
    | avg <= 0.200 = "Terrible Batting Average"
    | avg <= 0.250 = "Average Player"
    | otherwise = "You're doing great!"
    where avg = hits / atBats

getListItems :: [Int] -> String
getListItems [] = "list is empty."
getListItems (x:[]) = "list starts with " ++ show x
getListItems (x:y:[]) = "list contains " ++ show x ++ " and " ++ show y
getListItems (x:xs) = "1st item is " ++ show x ++ " and rest are " ++ show xs

getFirstItem :: String -> String
getFirstItem [] = "empty string"
getFirstItem all@(x:xs) = "The first letter in " ++ all ++ " is " ++ [x]

times4 :: Int -> Int
times4 x = x * 4
listTimes4 = map times4 [1,2,3,4,5]

mulBy4 :: [Int] -> [Int]
mulBy4 [] = []
mulBy4 (x:xs) = times4 x : mulBy4 xs


areStringsEq :: [Char] -> [Char] -> Bool
areStringsEq [] [] = True
areStringsEq (x:xs) (y:ys) = (x == y) && areStringsEq xs ys
areStringsEq _ _ = False

-- the input is a function that takes an Int and returns an Int
doMult :: (Int -> Int) -> Int
doMult func = func 3

num3Times4 = doMult times4


-- Int -> Int -> Int と区別ってつく？
getAddFunc :: Int -> (Int -> Int)
getAddFunc x y = x + y
adds3 = getAddFunc 3

lmbdTo10 = map (\x -> x * 3) [1,2,3,4,5]


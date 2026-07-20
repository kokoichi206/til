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


{-
    enumeration type
    https://hackage.haskell.org/package/enumerate-0.2.2/docs/Enumerate-Types.html

    BaseballPlayer という型の定義
    集合のイメージ。
    Pitcher, ... => データコンストラクタ, 値の生成子。
    代数的データ型。
-}
data BaseballPlayer = Pitcher
                    | Catcher
                    | Infielder
                    | Outfielder
            deriving Show

barryBonds :: BaseballPlayer -> Bool
barryBonds Outfielder = True
barryInOF = print(barryBonds Outfielder)


data Customer = Customer String String Double
    deriving Show
tomSmith :: Customer
tomSmith = Customer "Tom Smith" "123 Main" 25.50

getBalance :: Customer -> Double
getBalance (Customer _ _ b) = b

data RPS = Rock | Paper | Scissors
shoot :: RPS -> RPS -> String
shoot Rock Scissors = "Rock beats Scissors"
shoot Paper Rock = "Paper beats Rock"
shoot Scissors Paper = "Scissors beats Paper"
shoot Scissors Rock = "Scissors lose to Rock"
shoot Rock Paper = "Rock lose to Paper"
shoot Paper Scissors = "Paper lose to Scissors"
shoot _ _ = "Error: invalid input"

data Shape = Circle Float Float Float
            | Rectangle Float Float Float Float
            deriving Show
area :: Shape -> Float
area (Circle _ _ r) = pi * r ^ 2
area (Rectangle x1 y1 x2 y2) = (abs $ x2 - x1) * (abs $ y2 - y1)
-- area (Rectangle x1 y1 x2 y2) = (abs (x2 - x1)) * (abs (y2 - y1))
sumValue = putStrLn (show (1 + 2))

areaOfCircle = area (Circle 10 20 10)
areaOfRect = area (Rectangle 10 20 30 40)


-- type classes
-- (+) Num
data Employee = Employee {
    name :: String,
    position :: String,
    idNum :: Int
} deriving (Eq, Show)
samSmith = Employee {name = "Sam Smith", position = "Manager", idNum = 1001}
pam = Employee {name = "Pam", position = "Sales", idNum = 1002}
isSamPam = samSmith == pam

data ShirtSize = S | M | L
instance Eq ShirtSize where
    S == S = True
    M == M = True
    L == L = True
    _ == _ = False
instance Show ShirtSize where
    show S = "Small"
    show M = "Medium"
    show L = "Large"
smallAvailable = S `elem` [S,M,L]
theSize = show S


class MyEq a where
    areEqual :: a -> a -> Bool
instance MyEq ShirtSize where
    areEqual S S = True
    areEqual M M = True
    areEqual L L = True
    areEqual _ _ = False

sayHello = do
    putStrLn "Hello, what's your name?"
    name <- getLine
    putStrLn ("Hey " ++ name ++ ", you rock!")

fileName = "haskell-test.txt"
writeToFile = do
    theFile <- openFile fileName WriteMode
    hPutStrLn theFile "Random line of text"
    hClose theFile
readFromFile = do
    theFile <- openFile fileName ReadMode
    contents <- hGetContents theFile
    putStr contents
    hClose theFile


{-
    fib = [1,1,2,3,5,8,...]
    => tail fib = [1,2,3,5,8,...]
-}
fib = 1 : 1 : [a + b | (a, b) <- zip fib (tail fib)]
-- take 300th fib number
fib300 = fib !! 300

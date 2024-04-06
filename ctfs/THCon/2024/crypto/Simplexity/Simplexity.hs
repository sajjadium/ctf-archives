import GHC.Integer ( xorInteger )
import Data.Bifunctor ( bimap )
import Data.Char ( chr, ord )
import GHC.Num.Integer ( integerToInt, integerFromInt )

-- For this implementation, we consider the key length
-- equals to the length of the blocks
blockLength :: Int
blockLength = ?
initialVector :: String
initialVector = "?"
key :: String
key = "?"

-- XOR of blocks
charToInteger :: Char -> Integer
charToInteger = integerFromInt.ord
integerToChar :: Integer -> Char
integerToChar = chr.integerToInt
xorChar :: Char -> Char -> Integer
xorChar c1 c2 = xorInteger (charToInteger c1) (charToInteger c2)

xorblocks :: String -> String -> String
xorblocks b1 b2 = map integerToChar $ zipWith xorChar b1 b2

-- Vigenère for the case where the key length = blocks length
vigenere :: String -> String -> String
vigenere = zipWith (\k m -> chr $ ord 'a' + ((ord k + ord m - ord 'a') `mod` 26)) 

cipher :: String -> String
cipher = vigenere key

-- CBC
-- cbc :: iv -> blocks of clear text -> blocks of ciphered text
cbc :: String -> [String] -> [String]
cbc _ [] = []
cbc iv (b1:bs) = c1 : cbc c1 bs
    where c1 = cipher $ xorblocks iv b1

-- Vigenère + CBC
blocksFromText :: String -> [String]
blocksFromText [] = []
blocksFromText text = t : blocksFromText ts
        where (t, ts) = splitAt blockLength text

chall :: String -> String
chall s = concat.cbc initialVector $ blocksFromText s

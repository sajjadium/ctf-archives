import Control.Monad
import Data.List

-- Function to compute factorial
factorial :: Integer -> Integer
factorial n = product [1..n]

-- Function to generate Fibonacci sequence
fibonacci :: Int -> [Integer]
fibonacci n = take n fibs
    where fibs = 0 : 1 : zipWith (+) fibs (tail fibs)

main :: IO ()
main = do
    putStrLn "Factorial of 5:"
    print $ factorial 5

    putStrLn "First 10 Fibonacci numbers:"
    print $ fibonacci 10

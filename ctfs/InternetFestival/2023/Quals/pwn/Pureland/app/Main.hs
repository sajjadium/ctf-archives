module Main where

import Data.Primitive (sizeofMutableArray)
import Data.Primitive.ByteArray
  ( MutableByteArray,
    getSizeofMutableByteArray,
    mutableByteArrayContents,
    newByteArray,
    readByteArray,
    writeByteArray,
  )
import GHC.Exts (RealWorld)
import System.IO (hFlush, stdout)

menu :: MutableByteArray RealWorld -> IO ()
menu arr = do
  putStrLn "1. Write to array"
  putStrLn "2. Read from array"
  putStrLn "3. Calculate suffix sum"
  putStrLn "4. Exit"
  putStrLn "Enter your choice:"
  size <- getSizeofMutableByteArray arr
  hFlush stdout
  choice <- getLine
  case choice of
    "1" -> do
      putStrLn "Enter index: "
      hFlush stdout
      index <- getLine
      let pos = read index :: Int
      if checkBound pos size
        then putStrLn "Index out of bounds, what are you doing?"
        else do
          putStrLn "Enter value: "
          hFlush stdout
          value <- getLine
          writeByteArray arr pos (read value :: Int)
      menu arr
    "2" -> do
      putStrLn "Enter index: "
      hFlush stdout
      index <- getLine
      let pos = read index :: Int
      if checkBound pos size
        then putStrLn "Index out of bounds, what are you doing?"
        else do
          value <- readByteArray arr pos :: IO Int
          putStrLn $ "Value at index " ++ index ++ " is " ++ show value
      menu arr
    "3" -> do
      putStr "Calculating suffix sum..."
      suffixSum arr (size `div` 8 - 1) 0
      putStrLn "Done"
      menu arr
    "4" -> return ()
    _ -> do
      putStrLn "Invalid choice"
      menu arr
  where
    checkBound :: Int -> Int -> Bool
    checkBound pos size = pos >= (size `div` 8) || pos >= 65536 || pos < 0

    suffixSum :: MutableByteArray RealWorld -> Int -> Int -> IO ()
    suffixSum arr pos sum = do
      value <- readByteArray arr pos :: IO Int
      writeByteArray arr pos (sum + value)
      if pos < 0
        then return ()
        else suffixSum arr (pos - 1) (sum + value)

main :: IO ()
main = do
  arr <- newByteArray 128

  putStrLn "Welcome to pure land!"
  putStrLn "This program will let you write, read and calculate the suffix sum from an array of 16 integers."
  putStrLn "GLHF!"
  hFlush stdout

  menu arr
{-# LANGUAGE OverloadedStrings #-}
module Main where 

import Checker 
import Executor

import System.Exit ( exitSuccess, exitFailure )
import System.Environment ( getArgs )

compile :: FilePath -> FilePath -> IO ()
compile inp outp = do
  ex <- ghcCompile inp outp
  case ex of
    0 -> exitSuccess
    _ -> putStrLn "Compilation failed." >> exitFailure

main :: IO ()
main = do
  (inp_fp : out_fp : _) <- getArgs
  safe <- checkSecured inp_fp
  case safe of
    False -> do
      putStrLn "Your code is not secure enough."
      exitFailure
    True -> compile inp_fp out_fp  


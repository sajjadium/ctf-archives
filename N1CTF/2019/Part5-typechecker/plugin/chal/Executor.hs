{-# LANGUAGE OverloadedStrings #-}
module Executor ( ghcCompile ) where 

import System.Process ( readProcessWithExitCode )
import System.Posix.Process ( executeFile )
import GHC.IO.Exception ( ExitCode(..) )
import Control.Exception ( SomeException(..), throw )

compilerOption :: [String]
compilerOption = 
  [ "-XSafe"
  , "-XNoForeignFunctionInterface"
  , "-no-keep-o-files"
  , "-no-keep-hi-files"
  , "-w"
  , "-fplugin", "GHC.Types.Backdoor.Solver"   -- enable plugin
  ]

unEx :: ExitCode -> Int
unEx ExitSuccess = 0
unEx (ExitFailure err) = err 

runWithLimit :: [String] -> [String] -> IO Int
runWithLimit conf cmds = do
  (code, _, _) <- readProcessWithExitCode "prlimit" (conf ++ ["--"] ++ cmds) ""
  return $ unEx code 

-- compile a haskell program with specific 
ghcCompile :: FilePath -> FilePath -> IO Int 
ghcCompile src_fp out_fp = runWithLimit compiler_conf (["stack", "ghc", "--", "-o", out_fp] ++ compilerOption ++ [src_fp])
  where
    compiler_conf = ["--as=805306368", "--cpu=20"]


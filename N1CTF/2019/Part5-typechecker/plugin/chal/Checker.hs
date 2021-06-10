{-# LANGUAGE OverloadedStrings, ScopedTypeVariables #-}
module Checker ( checkSecured ) where

import HeaderInfo ( getImports, getOptionsFromFile )
import DynFlags
import SrcLoc ( unLoc )
import SysTools ( initSysTools, initLlvmConfig )
import StringBuffer ( hGetStringBuffer )
import FastString ( fsLit )
import Module ( moduleNameString )
import Outputable ( showPpr )
import GHC.Paths ( libdir )

import Control.Exception ( SomeException(..), try )
import Data.List ( elem )

myDynFlags :: IO DynFlags
myDynFlags = do
  emptySettings <- initSysTools (Just libdir)
  emptyLlvmConfig <- initLlvmConfig (Just libdir)
  return $ defaultDynFlags emptySettings emptyLlvmConfig

-- check option security
extractOptions :: FilePath -> IO [String]
extractOptions fp = do 
  dflags <- myDynFlags
  opts <- getOptionsFromFile dflags fp
  return $ map unLoc opts

allowedOptions :: [String]
allowedOptions = 
  [ "-XOverloadedStrings"   -- extensions allowed
  , "-XTypeFamilies"
  , "-XScopedTypeVariables"
  , "-XTupleSections"
  , "-XDataKinds"
  , "-XTypeFamilies"
  , "-XFlexibleContexts"
  , "-XFlexibleInstances"
  , "-XKindSignatures"
  , "-O0"                   -- compiler options allowed
  , "-O1"
  , "-O2"
  , "-O3"
  ]

isOptionsSafe :: FilePath -> IO Bool
isOptionsSafe fp = do
  opts <- extractOptions fp
  return $ all (\x -> elem x allowedOptions) opts 

-- check import security
extractImports :: FilePath -> IO [String]
extractImports fp = do 
  sb <- hGetStringBuffer fp
  dflags <- myDynFlags 
  (_, normimps, _) <- getImports dflags sb fp fp
  return $ map (\(_, modname) -> moduleNameString $ unLoc modname) normimps

allowedModules :: [String]
allowedModules = 
  [ "Prelude"               -- this is pretty limited, but still enough for the exploit
  , "GHC.Types.Backdoor"
  , "Data.Maybe"
  , "Data.Bits"
  , "Data.List"
  ]

isModulesSafe :: FilePath -> IO Bool
isModulesSafe fp = do
  mods <- extractImports fp
  return $ all (\x -> elem x allowedModules) mods

-- check whether the source code is secure enough
checkSecured :: FilePath -> IO Bool
checkSecured fp = do
  c1 <- try $ isOptionsSafe fp 
  c2 <- try $ isModulesSafe fp 
  let r1 = g c1
      r2 = g c2
  return $ r1 && r2
  where
    g c =
      case c of
        Left (err :: SomeException) -> False
        Right res -> res 


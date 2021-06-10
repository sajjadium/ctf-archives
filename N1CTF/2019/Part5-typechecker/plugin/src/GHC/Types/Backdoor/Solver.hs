{-# LANGUAGE OverloadedStrings #-}
module GHC.Types.Backdoor.Solver ( plugin ) where

import Data.Maybe ( mapMaybe )
import Debug.Trace ( trace )

import Plugins ( Plugin(..), defaultPlugin )
import Module ( mkModuleName )
import FastString ( fsLit )
import OccName ( mkTcOcc )
import TcPluginM ( TcPluginM, tcLookupTyCon, tcPluginTrace, tcPluginIO )
import TcRnTypes ( Ct(..), TcPlugin(..), TcPluginResult(..), ctEvidence, ctEvPred )
import TyCon ( TyCon(..) )
import TcEvidence ( EvTerm(..) )
import TyCoRep ( Type(..), TyLit(..) )

import Type ( PredTree(..), EqRel(..), classifyPredType )
import Outputable
import GHC.TcPluginM.Extra ( evByFiat, lookupModule, lookupName )

plugin :: Plugin
plugin = defaultPlugin { tcPlugin = \_ -> Just myPlugin }

myPlugin :: TcPlugin 
myPlugin = 
  TcPlugin { tcPluginInit = pluginInit
           , tcPluginSolve = pluginSolve
           , tcPluginStop = \_ -> return ()
           }

-- Find our custom tycon
pluginInit :: TcPluginM (TyCon, TyCon)
pluginInit = do
  mod <- lookupModule (mkModuleName "GHC.Types.Backdoor") (fsLit "backdoor")
  n1 <- lookupName mod $ mkTcOcc "B1"
  n2 <- lookupName mod $ mkTcOcc "B2"
  tc1 <- tcLookupTyCon n1
  tc2 <- tcLookupTyCon n2
  return (tc1, tc2)

-- Solve constraints
pluginSolve :: (TyCon, TyCon) -> [Ct] -> [Ct] -> [Ct] -> TcPluginM TcPluginResult
pluginSolve _ _ _ [] = return $ TcPluginOk [] [] 
pluginSolve (tc1, tc2) _ _ wanteds = do
  return $ TcPluginOk (mapMaybe (backdoorEquality tc1 tc2) wanteds) []

backdoorEquality :: TyCon -> TyCon -> Ct -> Maybe (EvTerm, Ct)
backdoorEquality tc1 tc2 ct = 
  case classifyPredType $ ctEvPred $ ctEvidence ct of
    EqPred NomEq t1 t2 -> 
      case bdrs t1 t2 of
        True -> Just (mkEv t1 t2, ct)
        False -> Nothing
    _ -> Nothing
  where
    mkEv t1 t2 = evByFiat "backdoor" t1 t2
    bdrs t1 t2 = (&&) (ofBackdoorTycon tc1 t1) $ ofBackdoorTycon tc2 t2

ofBackdoorTycon :: TyCon -> Type -> Bool
ofBackdoorTycon bdcon (TyConApp tycon [LitTy (NumTyLit i), _]) = (&&) (tycon == bdcon) (i == 1337)
ofBackdoorTycon _ _ = False


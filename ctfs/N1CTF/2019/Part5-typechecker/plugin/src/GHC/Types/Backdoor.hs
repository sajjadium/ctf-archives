{-# LANGUAGE DataKinds, KindSignatures #-}

module GHC.Types.Backdoor ( B1(..), B2(..) ) where

import GHC.TypeNats ( Nat(..) )

data B1 (a :: Nat) b = B1 { unB1 :: b }
data B2 (a :: Nat) b = B2 { unB2 :: b }


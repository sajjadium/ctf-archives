open! Core_kernel

val state_opt
  :  key:string
  -> (string option * (string option -> Bonsai.Event.t)) Bonsai.Computation.t

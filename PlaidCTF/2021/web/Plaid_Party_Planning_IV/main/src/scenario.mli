open! Core_kernel
open! Import

type t =
  { games : Game.t Game_id.Map.t
  ; people : Person.t Person_id.Map.t
  ; rooms : Room_id.Set.t
  }

val default : t

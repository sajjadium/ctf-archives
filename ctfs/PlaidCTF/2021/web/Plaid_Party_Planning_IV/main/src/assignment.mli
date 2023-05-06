open! Core_kernel
open! Import

type t =
  { games : Room_id.t option Game_id.Map.t
  ; people : Room_id.t option Person_id.Map.t
  }
[@@deriving bin_io, sexp, equal, fields]

val of_scenario : Scenario.t -> t
val rooms : all_rooms:Room_id.Set.t -> t -> Room.t Room_id.Map.t
val match_scenario : t -> Scenario.t -> Room.t Room_id.Map.t Uopt.t
val randomize : t -> Scenario.t -> t

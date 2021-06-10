open! Core_kernel
open! Import

type t =
  { people : unit Person_id.Map.t
  ; games : unit Game_id.Map.t
  }
[@@deriving equal, sexp]

module Full : sig
  type t =
    { people : Person.t Ids.Person_id.Map.t
    ; games : Game.t Ids.Game_id.Map.t
    }
end

val empty : t
val add_person : t -> Ids.Person_id.t -> t
val add_game : t -> Ids.Game_id.t -> t

open! Core_kernel
open! Import

type t =
  { people : unit Person_id.Map.t
  ; games : unit Game_id.Map.t
  }
[@@deriving equal, sexp]

module Full = struct
  type t =
    { people : Person.t Person_id.Map.t
    ; games : Game.t Game_id.Map.t
    }
end

let empty = { people = Person_id.Map.empty; games = Game_id.Map.empty }
let add_person t x = { t with people = Map.set t.people ~key:x ~data:() }
let add_game t x = { t with games = Map.set t.games ~key:x ~data:() }

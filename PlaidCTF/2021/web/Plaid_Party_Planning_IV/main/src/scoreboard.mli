open! Core_kernel

type t [@@deriving sexp_of]

module Entry : sig
  type t = Protocol.Scoreboard.Entry.t =
    { team : string
    ; score : float
    ; time : Time_ns.t
    }
end

val empty : t
val update : t -> Entry.t -> t
val updates : old:t -> new_:t -> Entry.t list
val fold : t -> init:'a -> f:('a -> Entry.t -> 'a) -> 'a

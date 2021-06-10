open! Core_kernel

type t =
  | Length of float
  | Complexity of float
  | Strategy of float
  | Luck of float
  | Cooperation of float
  | Deception of float
  | Unfriendly_knife_interaction of float
  | Triviality of float
  | Artistry of float
  | Num_players of (int * float) list
[@@deriving sexp, equal, variants]

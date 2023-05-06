open! Core_kernel

module Entry = struct
  type t = Protocol.Scoreboard.Entry.t =
    { team : string
    ; score : float
    ; time : (Time_ns.t[@sexp.opaque])
    }
  [@@deriving compare, sexp_of]

  let compare =
    Comparable.lexicographic
      [ Comparable.lift (Comparable.reverse Float.compare) ~f:(fun x -> x.score)
      ; Comparable.lift Time_ns.compare ~f:(fun x -> x.time)
      ; compare
      ]
  ;;

  include (val Comparator.make ~sexp_of_t ~compare)
end

type t =
  { by_team : Entry.t String.Map.t
  ; ordered : Set.M(Entry).t
  }
[@@deriving sexp_of]

let empty = { by_team = String.Map.empty; ordered = Set.empty (module Entry) }

let remove_team t team =
  match Map.find t.by_team team with
  | None -> t
  | Some orig ->
    { by_team = Map.remove t.by_team team; ordered = Set.remove t.ordered orig }
;;

let update t (entry : Entry.t) =
  if Set.mem t.ordered entry
  then t
  else (
    let t = remove_team t entry.team in
    { by_team = Map.add_exn t.by_team ~key:entry.team ~data:entry
    ; ordered = Set.add t.ordered entry
    })
;;

let updates ~old ~new_ = Set.diff new_.ordered old.ordered |> Set.to_list
let fold t ~init ~f = Set.fold t.ordered ~init ~f

open! Core_kernel
open! Bonsai_web
open! Bonsai.Let_syntax

module Model = struct
  type t =
    | None
    | Showing of bool * float
  [@@deriving sexp, equal]
end

module Action = struct
  type t =
    | Changed_by of float
    | Stop_showing
  [@@deriving sexp]
end

let track score =
  let%sub state, inject =
    Bonsai.state_machine0
      [%here]
      (module Model)
      (module Action)
      ~default_model:None
      ~apply_action:(fun ~inject:_ ~schedule_event:_ model action ->
        match model, action with
        | _, Stop_showing -> None
        | None, Changed_by value -> Showing (false, value)
        | Showing (b, _), Changed_by value -> Showing (not b, value))
  in
  let%sub watch_score =
    Bonsai.Edge.on_change'
      [%here]
      (module Float)
      score
      ~callback:
        (let%map inject = inject in
         fun prev next ->
           let prev = Option.value prev ~default:0. in
           inject (Changed_by (next -. prev)))
  in
  return
  @@ let%map state = state
     and () = watch_score
     and inject = inject in
     ( (match state with
       | None -> None
       | Showing (kind, value) -> Some (kind, value))
     , inject Stop_showing )
;;

let view score =
  let%sub score_change, stop_showing = track score in
  return
  @@ let%map score_change = score_change
     and stop_showing = stop_showing in
     Vdom.Node.div
       Vdom.Attr.
         [ (class_ "score-increment"
           @
           match score_change with
           | Some (true, _) -> class_ "show1"
           | Some (false, _) -> class_ "show2"
           | None -> empty)
           @ on_animationend (fun _ -> stop_showing)
         ]
       [ (match score_change with
         | None -> Vdom.Node.none
         | Some (_, score_change) -> Vdom.Node.textf "%+d" (Int.of_float score_change))
       ]
;;

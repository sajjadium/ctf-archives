open! Core_kernel
open! Bonsai_web
open! Bonsai.Let_syntax

module Model = struct
  type ('item, 'target) t =
    | Not_dragging
    | Dragging of 'item
    | Over_target of ('item * 'target * int)
  [@@deriving sexp, equal]
end

module Action = struct
  type ('item, 'target) t =
    | Start of 'item
    | End
    | Enter of 'target
    | Leave
    | Drop of 'target
  [@@deriving sexp]
end

type state =
  | Dragging
  | Not_dragging

type ('item, 'target) t =
  ('item, 'target) Model.t * (('item, 'target) Action.t -> Ui_event.t)

let apply_action
    ~inject:_
    ~schedule_event
    on_drop
    (model : (_, _) Model.t)
    (action : (_, _) Action.t)
    : (_, _) Model.t
  =
  match model, action with
  | Not_dragging, Start item -> Dragging item
  | Not_dragging, (End | Enter _ | Leave | Drop _) -> Not_dragging
  | Dragging _, End -> Not_dragging
  | Dragging item, Enter target -> Over_target (item, target, 1)
  | (Dragging _ as model), Leave -> model
  | Dragging _, Start item -> Dragging item
  | Over_target (_, target, count), Start item -> Over_target (item, target, count)
  | Over_target _, End -> Not_dragging
  | Over_target (item, _, count), Enter target -> Over_target (item, target, count + 1)
  | Over_target (item, target, count), Leave when count > 1 ->
    Over_target (item, target, count - 1)
  | Over_target (item, _, _), Leave -> Dragging item
  | Dragging item, Drop target | Over_target (item, _, _), Drop target ->
    (* what's another [schedule_event] between friends *)
    schedule_event (on_drop item target);
    Not_dragging
;;

let create
    (type item target)
    (module Item : Bonsai.Model with type t = item)
    (module Target : Bonsai.Model with type t = target)
    ~on_drop
  =
  Bonsai.state_machine1
    [%here]
    (module struct
      type t = (Item.t, Target.t) Model.t [@@deriving sexp, equal]
    end)
    (module struct
      type t = (Item.t, Target.t) Action.t [@@deriving sexp]
    end)
    ~apply_action
    ~default_model:Not_dragging
    on_drop
;;

let target
    (type target)
    (module Target : Bonsai.Model with type t = target)
    (t : ('item, target) t Bonsai.Value.t)
    ?(can_drop = Bonsai.Value.return true)
    target
  =
  let%pattern_bind model, inject = t in
  let attrs =
    let%map target_ = target
    and inject = inject in
    ( Vdom.Attr.(
        on_dragenter (fun _ -> inject (Enter target_))
        @ on_dragleave (fun _ -> inject Leave)
        @ on_dragend (fun _ -> inject End))
    , Vdom.Attr.(
        on_drop (fun _ ->
            Bonsai.Event.Many [ inject (Drop target_); Vdom.Event.Prevent_default ])
        @ on_dragover (fun _ -> Vdom.Event.Prevent_default)) )
  in
  let dragged_item =
    let%map target = target
    and model = model in
    match model with
    | Over_target (item, over, _) when Target.equal target over -> Some item
    | _ -> None
  in
  return
  @@ let%map attrs, if_can_drop = attrs
     and dragged_item = dragged_item
     and can_drop = can_drop in
     (if can_drop then Vdom.Attr.(attrs @ if_can_drop) else attrs), dragged_item
;;

let item
    (type item)
    (module Item : Bonsai.Model with type t = item)
    (t : (item, _) t Bonsai.Value.t)
    item
  =
  let%pattern_bind model, inject = t in
  let attrs =
    let%map item = item
    and inject = inject in
    Vdom.Attr.(on_dragstart (fun _ -> inject (Start item)) @ draggable true)
  in
  let state =
    let%map item = item
    and model = model in
    match model with
    | (Dragging drag | Over_target (drag, _, _)) when Item.equal drag item -> Dragging
    | _ -> Not_dragging
  in
  return
  @@ let%map attrs = attrs
     and state = state in
     attrs, state
;;

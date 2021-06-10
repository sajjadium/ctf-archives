open! Core_kernel
open! Bonsai_web
open! Bonsai.Let_syntax

module Model = struct
  type t =
    { next : int
    ; messages : string Int.Map.t
    }
  [@@deriving sexp, equal]
end

module Message_handle = struct
  type t = int [@@deriving sexp_of, equal]
end

module Action = struct
  type t =
    | Add_message of string
    | Clear_message of Message_handle.t
  [@@deriving sexp_of, equal]
end

type t = Action.t -> Message_handle.t Bonsai.Effect.t

let show act message = act (Action.Add_message message)

let remove act handle =
  act (Action.Clear_message handle)
  |> Bonsai.Effect.inject ~on_response:(fun _ -> Ui_event.Ignore)
;;

let view =
  let%sub model, act =
    Bonsai.actor0
      [%here]
      (module Model)
      (module Action)
      ~default_model:{ next = 0; messages = Int.Map.empty }
      ~recv:(fun ~schedule_event:_ model action ->
        match action with
        | Add_message message ->
          let id = model.next in
          ( { next = id + 1; messages = Map.add_exn model.messages ~key:id ~data:message }
          , id )
        | Clear_message handle ->
          { model with messages = Map.remove model.messages handle }, handle)
  in
  let%sub messages =
    Bonsai.assoc
      (module Int)
      (let%map model = model in
       model.messages)
      ~f:(fun key message ->
        return
        @@ let%map message = message
           and key = key
           and act = act in
           Vdom.Node.div
             ~key:(Int.to_string key)
             Vdom.Attr.[ class_ "info-messages-contents" ]
             [ Vdom.Node.text message
             ; Vdom.Node.div
                 Vdom.Attr.
                   [ class_ "close-info-messages" @ on_click (fun _ -> remove act key) ]
                 []
             ])
  in
  return
  @@ let%map messages = messages
     and act = act in
     Vdom.Node.div Vdom.Attr.[ id "info-messages" ] (Map.data messages), act
;;

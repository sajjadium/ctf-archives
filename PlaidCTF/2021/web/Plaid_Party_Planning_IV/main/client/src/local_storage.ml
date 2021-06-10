open! Core_kernel
open! Bonsai_web
open! Bonsai.Let_syntax
open Js_of_ocaml

let load_setting key =
  match Js.Optdef.to_option Dom_html.window##.localStorage with
  | None -> None
  | Some local_storage ->
    Js.Opt.case
      (local_storage##getItem (Js.string key))
      (fun () -> None)
      (fun v -> Some (Js.to_string v))
;;

let save_setting =
  let f =
    Bonsai.Effect.of_sync_fun (fun (key, data) ->
        match Js.Optdef.to_option Dom_html.window##.localStorage with
        | None -> ()
        | Some local_storage ->
          (match data with
          | None -> local_storage##removeItem (Js.string key)
          | Some data -> local_storage##setItem (Js.string key) (Js.string data)))
    |> unstage
  in
  fun key data -> f (key, data)
;;

let state_opt ~key =
  let%sub state, set_state =
    Bonsai.state_opt [%here] (module String) ?default_model:(load_setting key)
  in
  let assign =
    let%map set_state = set_state in
    fun new_value ->
      Ui_event.Many
        [ Bonsai.Effect.inject_ignoring_response (save_setting key new_value)
        ; set_state new_value
        ]
  in
  return
  @@ let%map state = state
     and assign = assign in
     state, assign
;;

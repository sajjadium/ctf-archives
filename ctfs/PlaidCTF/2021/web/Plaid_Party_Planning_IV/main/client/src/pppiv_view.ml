open! Core_kernel
open! Bonsai_web
open! Bonsai.Let_syntax
open! Pppiv_lib

module Which_view = struct
  type t =
    | Videoconference
    | Scoreboard
  [@@deriving sexp, equal, compare, enumerate]
end

let set_team_view ~set_team =
  let%sub input_state = Bonsai.state_opt [%here] (module String) in
  return
  @@ let%map set_team = set_team
     and input, set_input = input_state in
     Vdom.Node.div
       [ Vdom.Attr.class_ "set-team" ]
       [ Vdom_input_widgets.Entry.text
           ~value:input
           ~on_input:set_input
           ~placeholder:"Team name"
           ~extra_attrs:
             Vdom.Attr.
               [ on_keydown (fun ev ->
                     if ev##.keyCode = 13
                     then (
                       match input with
                       | Some team -> set_team team
                       | None -> Ui_event.Ignore)
                     else Ui_event.Ignore)
               ]
           ()
       ; Vdom_input_widgets.Button.with_validation
           "Set team"
           ~validation:(Result.of_option input ~error:"Enter a team name")
           ~on_click:set_team
       ]
;;

let navigation ~set_view =
  List.map
    Which_view.[ "Plan", Videoconference; "Scoreboard", Scoreboard ]
    ~f:(fun (name, which) ->
      Header.button
        ~on_click:
          (let%map set_view = set_view in
           fun _ -> set_view which)
        (Bonsai.Value.return name))
  |> Bonsai.Computation.all
;;

let application ~submit_assignment ~scoreboard =
  let%sub team, set_team = Local_storage.state_opt ~key:"team" in
  let%sub which_view, set_view =
    Bonsai.state [%here] (module Which_view) ~default_model:Videoconference
  in
  let%sub message_view, messages = Info_popup.view in
  let%sub main, center, right =
    Bonsai.enum
      (module Which_view)
      ~match_:which_view
      ~with_:(function
        | Videoconference ->
          (match%sub team with
          | None ->
            let%map.Bonsai.Computation main =
              set_team_view
                ~set_team:
                  (let%map set_team = set_team in
                   fun v -> set_team (Some v))
            in
            main, [], []
          | Some team ->
            let submit_assignment =
              let%map team = team
              and submit_assignment = submit_assignment in
              submit_assignment ~team
            in
            Videoconference.view ~submit_assignment ~messages)
        | Scoreboard ->
          let%map.Bonsai.Computation view = Scoreboard_view.view scoreboard in
          view, [], [])
  in
  let%sub navigation = navigation ~set_view in
  let%sub header = Header.view navigation center right in
  return
  @@ let%map main = main
     and header = header
     and message_view = message_view in
     Vdom.Node.div [] [ header; main; message_view ]
;;

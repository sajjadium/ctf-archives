open! Core_kernel
open! Bonsai_web
open! Bonsai.Let_syntax
open! Pppiv_lib

let view scoreboard =
  return
  @@ let%map scoreboard = scoreboard in
     Vdom.Node.div
       Vdom.Attr.[ class_ "scoreboard" ]
       ([ Vdom.Node.div Vdom.Attr.[ class_ "team" ] [ Vdom.Node.text "Team" ]
        ; Vdom.Node.div Vdom.Attr.[ class_ "score" ] [ Vdom.Node.text "Score" ]
        ]
       @ (Scoreboard.fold
            scoreboard
            ~init:(1, [])
            ~f:(fun (rank, acc) (entry : Scoreboard.Entry.t) ->
              ( rank + 1
              , [ Vdom.Node.div Vdom.Attr.[ class_ "sep" ] []
                ; Vdom.Node.div Vdom.Attr.[ class_ "rank" ] [ Vdom.Node.textf "%d" rank ]
                ; Vdom.Node.div
                    Vdom.Attr.[ class_ "team" ]
                    [ Vdom.Node.textf "%s" entry.team ]
                ; Vdom.Node.div
                    Vdom.Attr.[ class_ "score" ]
                    [ Vdom.Node.textf "%08.0f" entry.score ]
                ]
                :: acc ))
         |> snd
         |> List.rev
         |> List.concat))
;;

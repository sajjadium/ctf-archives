open! Core_kernel
open! Async_kernel
open! Bonsai_web
open Async_js
open Pppiv_lib

let submit_assignment ~conn =
  let dispatch input =
    let%bind.Deferred.Or_error conn = Connection.connected_or_failed_to_connect conn in
    Rpc.Rpc.dispatch Protocol.Submit_assignment.t conn input >>| Or_error.join
  in
  let dispatch = unstage (Effect.of_deferred_fun dispatch) in
  fun ~team assignment -> dispatch { team; assignment }
;;

let start_scoreboard_pipe conn =
  let%bind.Deferred.Or_error conn = Connection.connected_or_failed_to_connect conn in
  Rpc.Pipe_rpc.dispatch Protocol.Scoreboard.t conn ()
;;

let scoreboard ~conn =
  let var = Bonsai.Var.create Scoreboard.empty in
  Deferred.forever () (fun () ->
      match%bind start_scoreboard_pipe conn >>| Or_error.join with
      | Error err ->
        printf !"%{Error#hum}" err;
        Clock_ns.after (Time_ns.Span.of_sec 10.)
      | Ok (pipe, _) ->
        Pipe.iter' pipe ~f:(fun q ->
            let scoreboard = Bonsai.Var.get var in
            let scoreboard = Queue.fold q ~init:scoreboard ~f:Scoreboard.update in
            Bonsai.Var.set var scoreboard;
            return ()));
  Bonsai.Var.value var
;;

let run () =
  let conn = Connection.create () in
  let submit_assignment = submit_assignment ~conn in
  let scoreboard = scoreboard ~conn in
  let (_ : _ Start.Handle.t) =
    Start.start
      Start.Result_spec.just_the_view
      ~bind_to_element_with_id:"app"
      (Pppiv_view.application
         ~submit_assignment:(Bonsai.Value.return submit_assignment)
         ~scoreboard)
  in
  return ()
;;

open! Core
open! Async
open! Cohttp_async
open Pppiv_lib

let scenario = Scenario.default

module Writer_group = struct
  type 'a t = 'a Pipe.Writer.t Queue.t

  let create () = Queue.create ()

  let write t v =
    Queue.filter_inplace t ~f:(fun pipe ->
        if Pipe.is_closed pipe
        then false
        else (
          Pipe.write_without_pushback pipe v;
          true))
  ;;

  let add t pipe = Queue.enqueue t pipe
end

type t =
  { db_pool : ((module Caqti_async.CONNECTION), Caqti_error.t) Caqti_async.Pool.t
  ; mutable scoreboard : Scoreboard.t
  ; mutable scoreboard_group : Protocol.Scoreboard.Entry.t Writer_group.t
  ; mutable last_scoreboard_update : Time_ns.t
  ; mutable next_scoreboard_update : unit Deferred.t
  }

let of_caqti_error = function
  | Ok _ as x -> x
  | Error (`Error err) -> Error err
  | Error (#Caqti_error.t as e) -> Error (Error.of_lazy (lazy (Caqti_error.show e)))
;;

let with_db t f = Caqti_async.Pool.use f t.db_pool >>| of_caqti_error

let get_flag =
  let request =
    Caqti_request.find Caqti_type.unit Caqti_type.string "select flag from flag"
  in
  fun t -> with_db t (fun (module Db) -> Db.find request ())
;;

let sexp_type =
  Caqti_type.custom
    ~encode:(fun x -> Ok (Sexp.to_string_mach x))
    ~decode:(fun x ->
      try Ok (Sexp.of_string x) with
      | _ -> Error "Failed to decode sexp")
    Caqti_type.string
;;

let load_scoreboard =
  let request =
    Caqti_request.collect
      Caqti_type.unit
      Caqti_type.(tup3 ptime string float)
      "SELECT time, team, score FROM scoreboard"
  in
  fun t ->
    let%map.Deferred.Or_error entries =
      with_db t (fun (module Db) -> Db.collect_list request ())
    in
    List.map entries ~f:(fun (ptime, team, score) ->
        let time =
          Ptime.to_float_s ptime |> Time_ns.Span.of_sec |> Time_ns.of_span_since_epoch
        in
        { Scoreboard.Entry.time; team; score })
;;

let do_update_scoreboard t =
  let%bind () =
    Clock_ns.at (Time_ns.add t.last_scoreboard_update (Time_ns.Span.of_sec 1.))
  in
  match%map load_scoreboard t with
  | Error _ as err -> err
  | Ok entries ->
    let old_scoreboard = t.scoreboard in
    let new_scoreboard = List.fold ~init:old_scoreboard entries ~f:Scoreboard.update in
    List.iter
      (Scoreboard.updates ~old:old_scoreboard ~new_:new_scoreboard)
      ~f:(Writer_group.write t.scoreboard_group);
    t.last_scoreboard_update <- Time_ns.now ();
    t.scoreboard <- new_scoreboard;
    Ok ()
;;

let mark_scoreboard_stale t =
  if Deferred.is_determined t.next_scoreboard_update
  then (
    let updated = Ivar.create () in
    t.next_scoreboard_update <- Ivar.read updated;
    upon (do_update_scoreboard t) (fun result ->
        (match result with
        | Ok () -> ()
        | Error err ->
          Log.Global.info_s [%message "Failed to update scoreboard" ~_:(err : Error.t)]);
        Ivar.fill updated ()))
;;

let add_submission =
  let request =
    Caqti_request.exec
      Caqti_type.(tup4 string sexp_type float bool)
      "INSERT INTO submissions (team, assignment, score, flag_worthy) VALUES (?, ?, ?, ?)"
  in
  fun t ~team ~assignment ~score ~flag_worthy ->
    let%map result =
      with_db t (fun (module Db) ->
          Db.exec request (team, Assignment.sexp_of_t assignment, score, flag_worthy))
    in
    mark_scoreboard_stale t;
    let result =
      match result with
      | Ok _ -> result
      | Error err ->
        Log.Global.info_s [%message "Failed to submit" ~_:(err : Error.t)];
        Error (Error.of_string "Failed to submit")
    in
    result
;;

let get_scoreboard t =
  Rpc.Pipe_rpc.implement Protocol.Scoreboard.t (fun () () ->
      let pipe_r, pipe_w = Pipe.create () in
      Scoreboard.fold t.scoreboard ~init:pipe_w ~f:(fun pipe_w value ->
          Pipe.write_without_pushback pipe_w value;
          pipe_w)
      |> Writer_group.add t.scoreboard_group;
      Deferred.Or_error.return pipe_r)
;;

let handle_submission t =
  let open Deferred.Or_error.Let_syntax in
  Rpc.Rpc.implement Protocol.Submit_assignment.t (fun () { assignment; team } ->
      let open Protocol.Submit_assignment.Response in
      match Evaluate.is_complete scenario assignment with
      | false -> Invalid (Error.of_string "Incomplete assignment") |> return
      | true ->
        let score = Evaluate.evaluate scenario assignment in
        let flag_worthy = Float.O.(score > 1e20) in
        let%bind () = add_submission t ~assignment ~team ~score ~flag_worthy in
        let%map flag =
          match flag_worthy with
          | false -> return None
          | true ->
            let%map flag = get_flag t in
            Some flag
        in
        Valid { flag })
;;

let implementations state =
  Rpc.Implementations.create_exn
    ~implementations:[ handle_submission state; get_scoreboard state ]
    ~on_unknown_rpc:`Raise
;;

let http_handler ~docroot () ~body:_ _ (request : Request.t) =
  let uri = Cohttp.Request.uri request in
  match Uri.path uri with
  | "" | "/" ->
    Server.respond_with_file
      (Server.resolve_local_file ~docroot ~uri:(Uri.of_string "/index.html"))
  | _ ->
    let file = Server.resolve_local_file ~docroot ~uri in
    Server.respond_with_file file
;;

let main ~docroot ~port ~db_uri =
  let docroot = Filename.realpath docroot in
  let db_pool =
    Caqti_async.connect_pool ~max_size:10 db_uri |> of_caqti_error |> ok_exn
  in
  Log.Global.info_s
    [%message (port : int) (docroot : string) ~db_uri:(Uri.to_string db_uri)];
  let t =
    { db_pool
    ; scoreboard = Scoreboard.empty
    ; last_scoreboard_update = Time_ns.epoch
    ; next_scoreboard_update = return ()
    ; scoreboard_group = Writer_group.create ()
    }
  in
  mark_scoreboard_stale t;
  let%bind server =
    Rpc_websocket.Rpc.serve
      ~on_handler_error:`Ignore
      ~mode:`TCP
      ~where_to_listen:(Tcp.Where_to_listen.bind_to Localhost (On_port port))
      ~http_handler:(http_handler ~docroot)
      ~implementations:(implementations t)
      ~initial_connection_state:(fun () _ (_ : Socket.Address.Inet.t) _ -> ())
      ()
  in
  Cohttp_async.Server.close_finished server
;;

let command =
  Command.async
    ~summary:"start pppiv web server"
    [%map_open.Command
      let port =
        flag "port" (optional_with_default 8000 int) ~doc:"PORT serve on this port"
      and docroot =
        flag
          "docroot"
          (optional_with_default "." Filename.arg_type)
          ~doc:"DIRECTORY serve static files out of this directory"
      and db_uri =
        flag
          "db"
          (required (Arg_type.create Uri.of_string))
          ~doc:"URI connect to the database here"
      in
      fun () -> main ~docroot ~port ~db_uri]
;;

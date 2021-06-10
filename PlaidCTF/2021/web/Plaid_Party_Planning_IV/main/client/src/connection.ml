open Core_kernel
open Async_kernel
open Async_js
open Js_of_ocaml

module T = Persistent_connection_kernel.Make (struct
  module Address = Unit

  type t = Rpc.Connection.t

  let close t = Rpc.Connection.close t
  let is_closed = Rpc.Connection.is_closed
  let close_finished = Rpc.Connection.close_finished
end)

include T

type nonrec t =
  { somebody_cares : (unit, [ `Read | `Who_can_write of Perms.me ]) Bvar.t
  ; internal : t
  }

let connected_or_failed_to_connect t =
  Bvar.broadcast t.somebody_cares ();
  connected_or_failed_to_connect t.internal
;;

let uri () =
  let port =
    match Url.Current.port with
    | Some port -> port
    | None -> Url.default_http_port
  in
  let host = Url.Current.host in
  Uri.make ~scheme:"ws" ~host ~port ~path:"/ws" ()
;;

let create () =
  let somebody_cares = Bvar.create () in
  { somebody_cares
  ; internal =
      create
        ~server_name:"websocket"
        ~connect:(fun () ->
          let client = Rpc.Connection.client ~uri:(uri ()) () in
          match%map Clock_ns.with_timeout (Time_ns.Span.of_sec 10.) client with
          | `Timeout ->
            don't_wait_for
              (match%bind client with
              | Error _ -> return ()
              | Ok client -> Rpc.Connection.close client);
            Or_error.error_string "Timed out while connecting"
          | `Result result -> result)
        ~on_event:(fun event ->
          match event with
          | Disconnected | Failed_to_connect _ -> Bvar.wait somebody_cares
          | Obtained_address () | Attempting_to_connect | Connected _ -> return ())
        (fun () -> Deferred.Or_error.ok_unit)
  }
;;

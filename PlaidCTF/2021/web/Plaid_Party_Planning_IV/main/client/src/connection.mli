open Core_kernel
open Async_kernel
open Async_js

type t

val create : unit -> t
val connected_or_failed_to_connect : t -> Rpc.Connection.t Or_error.t Deferred.t

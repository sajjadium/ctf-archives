open! Core_kernel
open! Async_rpc_kernel

module Submit_assignment : sig
  module Query : sig
    type t =
      { team : string
      ; assignment : Assignment.t
      }
    [@@deriving bin_io, sexp, equal]
  end

  module Response : sig
    type t =
      | Invalid of Error.t
      | Valid of { flag : string option }
    [@@deriving bin_io, sexp, equal]
  end

  val t : (Query.t, Response.t Or_error.t) Rpc.Rpc.t
end

module Scoreboard : sig
  module Entry : sig
    type t =
      { team : string
      ; score : float
      ; time : Time_ns.t
      }
    [@@deriving bin_io]
  end

  val t : (unit, Entry.t, Error.t) Rpc.Pipe_rpc.t
end

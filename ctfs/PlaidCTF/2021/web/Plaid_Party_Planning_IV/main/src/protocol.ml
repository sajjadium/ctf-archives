open! Core_kernel
open! Async_rpc_kernel

module Submit_assignment = struct
  module Query = struct
    type t =
      { team : string
      ; assignment : Assignment.t
      }
    [@@deriving bin_io, sexp, equal]
  end

  module Response = struct
    type t =
      | Invalid of Error.t
      | Valid of { flag : string option }
    [@@deriving bin_io, sexp, equal]
  end

  let t =
    Rpc.Rpc.create
      ~name:"submit-assignment"
      ~version:2
      ~bin_query:[%bin_type_class: Query.t]
      ~bin_response:[%bin_type_class: Response.t Or_error.t]
  ;;
end

module Scoreboard = struct
  module Entry = struct
    type t =
      { team : string
      ; score : float
      ; time : Time_ns.t
      }
    [@@deriving bin_io]
  end

  let t =
    Rpc.Pipe_rpc.create
      ~name:"scoreboard"
      ~version:1
      ~bin_query:[%bin_type_class: unit]
      ~bin_response:[%bin_type_class: Entry.t]
      ~bin_error:[%bin_type_class: Error.t]
      ()
  ;;
end

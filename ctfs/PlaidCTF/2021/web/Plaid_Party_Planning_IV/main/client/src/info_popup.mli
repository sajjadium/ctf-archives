open! Core_kernel
open! Bonsai_web

module Message_handle : sig
  type t
end

type t

val show : t -> string -> Message_handle.t Bonsai.Effect.t
val remove : t -> Message_handle.t -> Ui_event.t
val view : (Virtual_dom.Vdom.Node.t * t) Bonsai.Computation.t

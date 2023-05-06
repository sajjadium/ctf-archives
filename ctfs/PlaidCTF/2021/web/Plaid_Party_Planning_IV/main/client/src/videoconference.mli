open! Core_kernel
open! Bonsai_web
open Pppiv_lib

val view
  :  submit_assignment:
       (Assignment.t -> Protocol.Submit_assignment.Response.t Or_error.t Bonsai.Effect.t)
       Bonsai.Value.t
  -> messages:Info_popup.t Bonsai.Value.t
  -> (Vdom.Node.t * Vdom.Node.t list * Vdom.Node.t list) Bonsai.Computation.t

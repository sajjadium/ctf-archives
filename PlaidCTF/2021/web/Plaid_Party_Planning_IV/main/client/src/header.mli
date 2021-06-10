open! Core_kernel
open! Bonsai_web
open Js_of_ocaml

val button
  :  ?enabled:bool Bonsai.Value.t
  -> on_click:(Dom_html.mouseEvent Js.t -> Ui_event.t) Bonsai.Value.t
  -> string Bonsai.Value.t
  -> Vdom.Node.t Bonsai.Computation.t

val view
  :  Vdom.Node.t list Bonsai.Value.t
  -> Vdom.Node.t list Bonsai.Value.t
  -> Vdom.Node.t list Bonsai.Value.t
  -> Vdom.Node.t Bonsai.Computation.t

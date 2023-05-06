open! Core_kernel
open! Bonsai_web
open Pppiv_lib

val view : Scoreboard.t Bonsai.Value.t -> Vdom.Node.t Bonsai.Computation.t

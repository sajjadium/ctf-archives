open! Core_kernel
open! Bonsai_web
open! Pppiv_lib

val application
  :  submit_assignment:
       (team:string
        -> Assignment.t
        -> Protocol.Submit_assignment.Response.t Or_error.t Bonsai.Effect.t)
       Bonsai.Value.t
  -> scoreboard:Scoreboard.t Bonsai.Value.t
  -> Vdom.Node.t Bonsai.Computation.t

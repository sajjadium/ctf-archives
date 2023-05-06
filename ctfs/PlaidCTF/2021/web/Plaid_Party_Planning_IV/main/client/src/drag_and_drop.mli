open! Bonsai_web

type state =
  | Dragging
  | Not_dragging

type ('item, 'target) t

val create
  :  (module Bonsai.Model with type t = 'item)
  -> (module Bonsai.Model with type t = 'target)
  -> on_drop:('item -> 'target -> Bonsai.Event.t) Bonsai.Value.t
  -> ('item, 'target) t Bonsai.Computation.t

val target
  :  (module Bonsai.Model with type t = 'target)
  -> ('item, 'target) t Bonsai.Value.t
  -> ?can_drop:bool Bonsai.Value.t
  -> 'target Bonsai.Value.t
  -> (Vdom.Attr.t * 'item option) Bonsai.Computation.t

val item
  :  (module Bonsai.Model with type t = 'item)
  -> ('item, 'target) t Bonsai.Value.t
  -> 'item Bonsai.Value.t
  -> (Vdom.Attr.t * state) Bonsai.Computation.t

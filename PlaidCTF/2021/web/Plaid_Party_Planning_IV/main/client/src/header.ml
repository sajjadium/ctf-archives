open! Core_kernel
open! Bonsai_web
open! Bonsai.Let_syntax

let button ?(enabled = Bonsai.Value.return true) ~on_click text =
  return
  @@ let%map enabled = enabled
     and action = on_click
     and text = text in
     Vdom.Node.div
       Vdom.Attr.
         [ (class_ "action" @ if not enabled then class_ "disabled" else on_click action)
         ]
       [ Vdom.Node.text text ]
;;

let view left center right =
  return
  @@ let%map left = left
     and center = center
     and right = right in
     Vdom.Node.div
       Vdom.Attr.[ class_ "header" ]
       ([ Vdom.Node.div Vdom.Attr.[ class_ "left-side" ] left ]
       @ center
       @ [ Vdom.Node.div Vdom.Attr.[ class_ "right-side" ] right ])
;;

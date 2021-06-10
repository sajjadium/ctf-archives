open! Core_kernel
open! Import

type video =
  { src : string
  ; content_type : string
  }
[@@deriving sexp_of]

type t =
  { id : Person_id.t
  ; name : string
  ; criteria : (Game_attribute.t * float) list
  ; avatar : video list
  }
[@@deriving fields, sexp_of]

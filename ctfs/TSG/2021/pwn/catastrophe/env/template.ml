(* thank you @strikeskids :pray: *)
open struct
  let blocked = `Blocked

  module Blocked = struct
    let blocked = blocked
  end
end
module Fixed_bytes = struct
    include Bytes

    let unsafe_blit = blocked
    let unsafe_blit_string = blocked
    let unsafe_fill = blocked
    let unsafe_get = blocked
    let unsafe_set = blocked
    let unsafe_of_string = blocked
    let unsafe_to_string = blocked
end

(* Present for you *)
open Printf
open Fixed_bytes
(* :) *)

/** code **/


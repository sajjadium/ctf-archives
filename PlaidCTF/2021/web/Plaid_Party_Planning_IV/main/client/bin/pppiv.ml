open! Async_kernel

let () =
  Async_js.init ();
  don't_wait_for (Pppiv_client_lib.Main.run ())
;;

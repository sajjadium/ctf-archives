by Hidden Investigations
Reverse Engineering
Vaelorhand Online guards its ranked ladder with a server-side anti-cheat module. Before the backend accepts a match result, the session server feeds each client's submitted session-integrity token through this module. Only a token the module accepts lets the result stand.

The match/session tier runs on the BEAM (Erlang), and the anti-cheat ships as a single compiled, stripped .beam module with no source. A build leaked. Recover the one token the validator accepts; accepting it unlocks the flag.

It is an ordinary BEAM module named signal_lock. Drop the file in a directory, start a shell with that directory on the code path, and call its exported entry point with your candidate token:

$ erl -pa .
1> signal_lock:module_info(exports).
2> signal_lock:verify(YourToken).
A correct token returns {ok, <<"hiCTF{...}">>}; anything else stays locked. Requires Erlang/OTP 26 or newer: older runtimes cannot load the module and fail with an unsupported-opcode error.

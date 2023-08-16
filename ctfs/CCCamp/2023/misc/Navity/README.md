I made this cool bare metal arm firmware that can calculate a the fib number for a given input. You have to use ncat -C to talk to the application.
You can also connect to another exposed port by changing the ncat command.
ncat -C --ssl 84d765a3391925f34bbb1223-1024-navity.challenge.master.camp.allesctf.net 31337 -> ncat -C --ssl 84d765a3391925f34bbb1223-1234-navity.challenge.master.camp.allesctf.net 31337 to connect to port 1234.
You have to create a new session after each run :)

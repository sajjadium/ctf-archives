Let's pretend I just learned about this cool thing called RPC and wrote a simple example! Is it secure?
nc tictac.nc.jctf.pro 1337
Note: do not focus on run.sh, nsjail.cfg or the Dockerfile: those are there to host and jail/sandbox the challenge properly. Note2: If you get a Couldn't initialize cgroup 2 user namespace for pid=... in container logs, you lack cgroups v2 - you can mitigate this by commenting out use_cgroupv2, group_pids_max, cgroup_mem_max, cgroup_cpu_ms_per_sec lines in nsjail.cfg.


Here's an example how you can play the game!

```
tictactoe:new_game 0 0 0 0 0 0
tictactoe:computer_turn 0 0 0 0 0 0
tictactoe:player_turn 1 1 0 0 0 0
tictactoe:computer_turn 0 0 0 0 0 0
tictactoe:player_turn 2 1 0 0 0 0
tictactoe:computer_turn 0 0 0 0 0 0
tictactoe:player_turn 2 2 0 0 0 0
tictactoe:computer_turn 0 0 0 0 0 0
tictactoe:player_turn 0 0 0 0 0 0
tictactoe:computer_turn 0 0 0 0 0 0
tictactoe:print 0 0 0 0 0 0
```

It looks very useful, doesn't it?

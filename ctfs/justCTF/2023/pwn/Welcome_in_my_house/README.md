r3kapig
May the Force be with you.
nc house.nc.jctf.pro 1337
Note: do not focus on run.sh, nsjail.cfg or the Dockerfile: those are there to host and jail/sandbox the challenge properly. Note2: If you get a Couldn't initialize cgroup 2 user namespace for pid=... in container logs, you lack cgroups v2 - you can mitigate this by commenting out use_cgroupv2, group_pids_max, cgroup_mem_max, cgroup_cpu_ms_per_sec lines in nsjail.cfg.

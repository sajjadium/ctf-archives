#!/bin/sh
echo -n 'mode:LISTEN hostname:"app" cwd:"/app" port:5000 max_conns:0 max_conns_per_ip:1 time_limit:60 rlimit_as_type:HARD rlimit_cpu_type:HARD rlimit_fsize_type:HARD rlimit_nofile_type:HARD rlimit_fsize: 50 rlimit_nofile: 50 mount:{src:"/srv" dst:"/" is_bind:true nosuid:true nodev:true} cgroup_mem_max:20971520 cgroup_mem_swap_max:0 cgroup_cpu_ms_per_sec:100 cgroupv2_mount:"/jail/cgroup/unified/run" use_cgroupv2:true exec_bin:{path:"/app/run"} mount { dst: "/app/quizzes" fstype: "tmpfs" rw: true }' > /tmp/nsjail.cfg


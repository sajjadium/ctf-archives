FROM tsuro/nsjail
COPY challenge/namespaces /home/user/chal
#COPY tmpflag /flag
CMD /bin/sh -c "/usr/bin/setup_cgroups.sh && cp /flag /tmp/flag && chmod 400 /tmp/flag && chown user /tmp/flag && su user -c '/usr/bin/nsjail -Ml --port 1337 --chroot / -R /tmp/flag:/flag -T /tmp --proc_rw -U 0:1000:1 -U 1:100000:1 -G 0:1000:1 -G 1:100000:1 --keep_caps --cgroup_mem_max 209715200 --cgroup_pids_max 100 --cgroup_cpu_ms_per_sec 100 --rlimit_as max --rlimit_cpu max --rlimit_nofile max --rlimit_nproc max -- /usr/bin/stdbuf -i0 -o0 -e0 /usr/bin/maybe_pow.sh /home/user/chal'"

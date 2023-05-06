We recreated CVE-2016-2383. Your task is to read out the variable named uiuctf_flag in the kernel memory, by building an arbitrary kernel memory read via a malicious eBPF program. Use of provided starter code is optional; if you have better methods feel free to use them instead.

$ stty raw -echo; nc bpf-badjmp.chal.uiuc.tf 1337; stty -raw echo

Upload large files to VM: $ nc bpf-badjmp.chal.uiuc.tf 1338 < file

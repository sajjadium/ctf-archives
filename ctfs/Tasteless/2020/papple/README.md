Q&A

    Q: How do I run this locally

A: Using docker:

xz --decompress papple.dsk.xz
docker build -t  tasteless/papple .
docker run -it --env IP=${YOUR_IP} --env FLAG=tstlss{this_is_your_local_test_flag!} -p 5900:5900  tasteless/papple

You can also pull tasteless/papple from DockerHub.

    Q: The docker container crashes with "ERROR: Cannot map Low Memory Globals: Operation not permitted.".

A: The challenge depends on mmap_min_addr=0. Run sysctl -w vm.mmap_min_addr="0" do disable it temporarily, or sudo bash -c "echo 0 > /proc/sys/vm/mmap_min_addr" to disable it permamently (not recommended!)

    Q: But how do I connect locally

A: In tasteless CTF, you no connect to challenge, challenge connect to you on port 1337.

    Q: how do I desktop?

VNC on port 5900. The password is tasteless.

    Q: where is the challenge?

Click on the papple drive, then on System Folder and Startup Items.

    Q: ipv6

A: No.

    Q: My Emulator keeps crashing.

A: Yes.


# pwn / flag sharing

nsjail (and wrappers around it, such as redpwn/jail) are popular tools used to
jail CTF challenges, and you'll find it used to jail many of our pwn challenges.

For most pwn challenges, you're connecting to the same port as everyone else
and (in most cases) are running code on the same CPU. nsjail ensures that your
connection does not impact other users by (among other things) providing a
sandboxed filesystem and enforcing strict resource limits. 

But what if jails share more than you think?

### Remote setup

***It is recommended that you test and develop your exploit against our remote.***

Remote is running in a t2.{xlarge/2xlarge/4xlarge} on AWS. Other instance types
will have different behavior (though it is likely solvable on most of them).

When you connect to remote, you are connecting to an "instancer" which will
direct you to a personal instance of the challenge container. Pay attention
to the IP and port provided by the instancer, as it may change.

A template is provided in solve-template.py

### Local setup

It is not recommended that you run the challenge locally, but everything is here
if you wish to do so. There ***will*** be important differences between your local
setup and remote which ***will*** break your solution.

Local setup is not recommended, but if you want to run it, run `./runme.sh`.

### Tips

- You are not intended to exploit the instancer. If you do, please contact the admins.
- The "t2" family of AWS instances has intel-based processors with an inclusive, shared, L3 cache.

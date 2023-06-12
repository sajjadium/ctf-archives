A vulnerability has been introduced into the v8 engine.
Your goal is to trigger the vulnerability, to achieve a read primitive and use that to read the flag from the memory.
We are providing:
v8 compiled with the vulnerability
Dockerfile that you can use to run the engine (you need to run it with --privileged to work properly)
A fake flag for you to try and read
patch.patch That shows the vulnerability we introduced
run which is the v8 runner - allowing you to see the flow and the flag loading
snapshot_blob.bin a binary to runs the v8 engine (provides its environment)
As the challenge is quite complex, we will be awaring it a big amount of points.
As there is no easy way to run it in a secure environment - once you have solved it - send the solution to: info@typhooncon.com
Solution MUST contain:
Javascript code that solves challenge
A technical writeup of what you are doing, where/what the vulnerability is, how you exploit it - it must show root cause analysis of the vulnerability, it must show how you are exploiting the vulnerability to reveal the flag

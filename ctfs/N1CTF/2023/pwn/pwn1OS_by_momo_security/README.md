pwn1OS payload submit：
curl http://152.136.46.174:1024/n1ctf/submit?team=<team_name>&urlscheme=<base64(payload)>
Example:
curl http://152.136.46.174:1024/n1ctf/submit?team=wangwangdui&urlscheme=bjFjdGY6Ly8=


Queries whether the submitted payload has completed execution:
curl http://152.136.46.174:1024/n1ctf/query?taskid=<taskid>
Example:
curl http://152.136.46.174:1024/n1ctf/query?taskid=820f7b79e1206ce0de4c7c2cb4d27d10</code>
// Prohibit attacks on this task such as Brute-force, penetration, etc.

momo security bounties apply to this challenge.

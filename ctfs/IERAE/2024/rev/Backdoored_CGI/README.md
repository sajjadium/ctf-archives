authored by hugeh0ge

So, it was found that one of my colleagues was an industrial spy... The spy was in charge of implementing a CGI used in our company product. Luckily, the CGI was still under development, which means we had no actual damage.

Nevertheless, I'm very curious what the spy have done. When I execute the CGI with ENABLE_DEBUG_CGI=1 ./setting.cgi "500 test", it somehow spawns a shell while it's originally supposed to just throw `1` as exception. Therefore, it's obvious that the spy patched somewhere in the CGI. But I can't see any diff in the disassembly. For your information, I attached both the original binary and the one patched by the spy. If you don't trust me, you can bindiff them. You can confirm that there's nothing different. Where did he change stealthily? Help me find out what's going on...

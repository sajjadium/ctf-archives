The engineers at SIGPwny Inc. wants to retaliate against PwnySIG Inc. for finding their secrets. They found PwnySIG Inc.'s server and was able to detach its hard drive and replace the kernel with a backdoor-ed kernel.

Unfortunately, they soon discovered that the server has secure boot on, and there's no firmware setup to disable it... how would it be possible to boot this backdoor kernel? Hmm... what's this? How considerate of PwnySIG Inc. to leave a signed lua interpreter wide open. Maybe they can bypass secure boot through that?

$ socat file:$(tty),raw,echo=0 openssl:lua-efi.chal.uiuc.tf:1337

author: YiFei Zhu

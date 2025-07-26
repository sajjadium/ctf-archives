The engineers at SIGPwny Inc. is up to some shenanigans again in SMM. They totally thought it was safe to expose the write API of SmmLockBox to the OS. Unfortunately the secrets (flag) at physical address 0x44440000 got leaked again, and it's only readable from SMM! How was this possible?

author: YiFei Zhu

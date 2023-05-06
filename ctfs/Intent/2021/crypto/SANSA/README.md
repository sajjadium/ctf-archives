# SANSA

It is well known that RSA and even EC-DSA are not to be trusted. But how would we deploy software updates without pubic key cryptography? This is why our research group has created a new zero-knowledge scheme just for you. We are glad to present the Secure Authentication of New Software Amendments (SANSA). Our server awaits your updates! Just POST to /sansa_update with {"content": <base64 encoding of the update file>, "signature": <SANSA signature>}.  

Kshitij Raj

An EC2 instance in our web tier was found running an unauthorised scheduled script, /opt/agent/vault.py, installed right after an SSH login from an address nobody recognised. The script keeps its configuration in an encrypted vault — and the key isn't stored on disk. It's derived at runtime from the instance's own identity.

We pulled the script, the vault, and the host logs. Review the code, work out how the vault is keyed, and recover the operator's configuration note.

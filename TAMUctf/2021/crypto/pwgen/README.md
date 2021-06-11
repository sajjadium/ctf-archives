We're trying to figure out the current password of REDACTED. We have reason to believe that they generated a set of passwords at the same time using a custom password generation program and that their previous password was ElxFr9)F. Can you figure out their current password?
src/main.rs
openssl s_client -connect tamuctf.com:443 -servername pwgen -quiet

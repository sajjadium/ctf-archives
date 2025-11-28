easy windows
The SOC of the Ministry of Magic received multiple critical alerts from the Domain Controller.

Everything seems to be out of control.

It seems that a critical user has been compromised and is performing nasty magic using the DCsync spell.

You're mandated to investigate the Principal Domain Controller event logs to find:
- sAMAccountName (lowercase) of the compromised account performing bad stuff.
- Timestamp of the beginning of the attack, format: DD/MM/YYYY-11:22:33 SystemTime.
- Source IP address used for this attack.
- The last legitimate IP used to login before the attack.

The findings have to be separated by a ";".

Here is an example flag format:

Hero{john.stark;DD/MM/YYYY-11:22:33;127.0.0.1;127.0.0.1}

Format: ^Hero{\S+}$
Author: xThaz

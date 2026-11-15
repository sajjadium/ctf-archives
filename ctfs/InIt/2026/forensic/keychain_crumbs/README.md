Kshitij Raj

Marcus Reid, a senior developer at Tanvoro Systems — a studio that builds macOS and iOS software — installed a "cracked" copy of a paid productivity app from an unofficial mirror after his trial expired. Minutes later his MacBook began reaching out to an unfamiliar host posing as an Apple iCloud service. Our network sensor flagged the anomaly and captured full traffic before the workstation could be isolated.

Triage confirmed an information-stealer had swept Marcus's home directory — browser credentials, his login Keychain, and system data — and shipped it to an attacker-controlled server. Stakeholders need to know exactly what left the network. Threat intel believes the operators were careless: they tunnelled everything over plaintext HTTP, and one stolen item appears to carry a secret the attacker meant to keep hidden.

You have one artifact — the packet capture from the incident. Reconstruct what the stealer exfiltrated, profile the compromised host, and recover the secret the attackers accidentally leaked in the clear.

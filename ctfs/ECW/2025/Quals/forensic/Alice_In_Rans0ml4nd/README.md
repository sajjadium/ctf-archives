You are urgently contacted by Alice-Corp, a company specialized in developing technological solutions. Our server as well as all workstations connected to our Active Directory have suddenly been encrypted. The Alice-Corp network team managed to capture part of the network traffic. As a forensic investigator, you must analyze this file to find:

The email address used by the attacker (format: attacker@example.com)
The email address targeted within the company (format: victim@alice.corp)
The MD5 hash of the first malware
The domain name contacted to download a script
The password used to connect to the server
The name of the scheduled task that was executed
The domain name (in lowercase) contacted by the script to download the second malware
The MD5 hash of the malware present on the server
The domain name used for data exfiltration
The name of the ransomware gang (in lowercase)
The cryptocurrency wallet address used by the attackers
The final flag contained in a file exfiltrated by the malware
Then create a sha256 digest. example echo -n "totor@example.com:roro@alice.corp:5d41402abc4b2a76b9719d911017c592:example.com:123456789:ImAtask:example.com:5d41402abc4b2a76b9719d911017c592:example.com:black-cat:84EgZVjXKF4d1JkEhZSxm4LQQEx64AvqQEwkvWPtHEb5JMrB1Y86y1vCPSCiXsKzbfS9x8vCpx3gVgPaHCpobPYqQzANTnC:fin4l_flag" | sha256sum

ECW{976605e64af03242e3321d7b5cdb8c6bb0bd0839ca36ba12abb11cef0fdac320}

Disclaimer The PCAP file provided in this challenge contains real or simulated malicious payloads (such as executables, scripts, or infected files transferred over the network).
Use an isolated environment
Archive password : 1_C0ns3nt_;)

Challenge made by Insomnia from :

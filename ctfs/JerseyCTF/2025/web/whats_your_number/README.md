hard networking

Noah Jacobson

Anna found this strange website. We do not know much about it but would like to see what we could find. She told me that something strange is happening on the transport layer, can you find out more?

This challenge requires the ability to spoof source IP addresses. Some ISPs will block this. To help keep the challenge fair, we've setup a relay. Sending a packet to whats-your-number-relay.aws.jerseyctf.com (resolve the IP address) will rewrite the source address to 1.2.3.4 and forward it to whats-your-number.aws.jerseyctf.com. Nothing else is changed besides the source and destination IP address.

Please note that being behind a NAT or firewall may still prevent the required packets from going through. If you encounter this, you may need to use a cloud provider or VPN that provides direct access to a public IP address. You may want to practice in your LAN first.

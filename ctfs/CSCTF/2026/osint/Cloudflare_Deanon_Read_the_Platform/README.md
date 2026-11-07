OSINT
Easy
covert-security
AUTHOR
Covert Security
MISSION
BRIEFING
🪺 Putting a scam behind Cloudflare hides its address from victims, and from the investigators chasing it. NestEgg Capital promises guaranteed returns and delivers withdrawal fees. The site sits behind a proxy so nobody can see where it is hosted.
Scope: simulated environment. Stay passive. Only the target domain and the single host you identify are in scope.
Internal fraud alert:

Over six weeks, 14 customers wired EUR 212,000 to NestEgg Capital. The cybercrime unit can only act on the hosting provider. The site sits behind Cloudflare. Find the real server. — Anneliese Brandt, Head of Fraud Intelligence, Marrowgate Savings Bank

**Call note 2291-07** (excerpt):
> Customer says the investment site is https://cs-adwi-covsec-lab-1.eu and that it is "licensed by the Lower Dunwich Financial Supervisory Board". Customer was told that withdrawals require a "small processing fee" and has now paid it four times.
**Task 1 — Read the Platform**
Find the company registration number advertised by the NestEgg Capital platform.
**Answer**: the registration number.
Flag format: `CSCTF{}`

Answer boundary: Submit the registration number exactly as it is displayed by the simulated NestEgg public site. Do not substitute a registry lookup, a historical result, or a guessed value.

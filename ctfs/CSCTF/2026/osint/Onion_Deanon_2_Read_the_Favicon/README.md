OSINT
Easy
covert-security
AUTHOR
Covert Security
MISSION
BRIEFING
🕊️ Even a server that only wants to be reached through Tor still tells the world a little about itself. DarkPigeon runs its victim negotiation portal as a Tor hidden service — onion routing only, no clearnet domain. Whether that is enough is for you to find out.
Scope: simulated environment. Reach the onion service with Tor Browser. Stay passive. Only the single host you identify is in scope.
Forum post:

[ DARKPIGEON ] NEW VICTIM: Coop & Crumb Birdseed Wholesalers
87 GB. Supplier contracts, customer database, payroll.
Victim portal (Tor Browser): http://schpqwdfzcmdcbim7w24jj5ph5h6fqvcbj5zhkhof3z3v75ydljkzsad.onion

**IR client email**:
> We've been hit by DarkPigeon and need to know where their portal is hosted so our lawyers can file a takedown. Please tell us what you find. > — Ottilie Crumb, IT Manager, Coop & Crumb
**Task 1 — Read the Favicon**
Obtain the favicon served by the DarkPigeon portal and hash it the way Shodan does.
**Answer**: the favicon hash, as a signed integer.
Flag format: `CSCTF{}`

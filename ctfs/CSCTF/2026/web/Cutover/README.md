Web
Hard
AUTHOR
Mohamed Amine Mzoughi
MISSION
BRIEFING
Marenth's real-time settlement rail, run by the Central Settlement Authority (MCSA), closes its value day at 16:00, and coalition partners clear their local payments over the same rail. Eleven batches are queued for the cutover window and one was planted by Glass Tide; if it settles as queued it drains the sovereign liquidity buffer below its floor and the authority has to suspend the rail.

The duty console runs at OPERATOR tier, and recalling a queued batch needs SUPERVISOR. Find the hostile batch and get a recall accepted while the cutover window is still open; the recall receipt carries the authorization code. The settlement engine source ships as engine-src.tar.gz for audit (the console also serves it at /source/engine-src.tar.gz) and matches the build the rail runs. The API, the manifest wire format and the error taxonomy are published at /api/v1/schema.

Flag format: CSCTF{...}

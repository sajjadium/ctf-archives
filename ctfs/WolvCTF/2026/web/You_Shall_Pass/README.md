ulisesalan

An authentication service asks you to log in with a user and token. It checks every submitted token against a signature on file. Admin access is ordinarily off limits, but does the verifier really check every token before admitting a login?

Send a POST request to /login with a JSON body containing a user and a token.

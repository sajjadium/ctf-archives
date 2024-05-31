13x1

These XSS vectors are getting ridiculous! So I made a secure note app. The only NPM dependency is DOMPurify, and I directly store the output of DOMPurify.sanitize and serve that back, so it has to be secure, right? It's barely 16 LoC!

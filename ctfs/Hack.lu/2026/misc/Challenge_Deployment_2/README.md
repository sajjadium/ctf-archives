misc
kubernetes

First Implementation was broken. Now we hardened the permissions a bit.

To access the UI, run: kubectl proxy --port=8080 then open http://localhost:8080/api/v1/namespaces/ctf/services/http:ui:80/proxy/ in your browser.

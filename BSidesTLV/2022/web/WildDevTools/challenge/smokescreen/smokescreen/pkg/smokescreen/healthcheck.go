package smokescreen

import (
	"net/http"
)

// HealthcheckMiddleware allows a user defined http.Handler to be invoked by
// requests to the /healthcheck endpoint. This function is set in the
// smokescreen config.
type HealthcheckMiddleware struct {
	Proxy       http.Handler
	Healthcheck http.Handler
}

func (h HealthcheckMiddleware) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path == "/healthcheck" {
		h.Healthcheck.ServeHTTP(w, r)
	} else {
		h.Proxy.ServeHTTP(w, r)
	}
}

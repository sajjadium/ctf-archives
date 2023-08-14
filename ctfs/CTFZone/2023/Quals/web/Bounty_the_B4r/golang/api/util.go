package api

import (
	"context"
	"encoding/json"
	"net/http"
	"strings"

	"github.com/go-chi/jwtauth/v5"
	"github.com/lestrrat-go/jwx/v2/jwt"
	"github.com/rs/zerolog/log"
)

const (
	GenericError uint64 = 1
)

var JwtSecret string

func Ptr[T any](v T) *T {
	return &v
}

func EncodeResponse(w http.ResponseWriter, resp interface{}) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

func HandleError(err error, w http.ResponseWriter) {
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		resp := GenericResponse{
			Error:   Ptr(GenericError),
			Message: Ptr(err.Error()),
		}
		EncodeResponse(w, resp)
	}
}

func HandleNotFound(w http.ResponseWriter) {
	w.WriteHeader(http.StatusNotFound)
}

func HandleNoError(w http.ResponseWriter) {
	const NO_ERROR uint64 = 0
	const NO_ERROR_MSG string = "No error"

	resp := GenericResponse{
		Error:   Ptr(NO_ERROR),
		Message: Ptr(NO_ERROR_MSG),
	}
	EncodeResponse(w, resp)
}

func Authenticator(ja *jwtauth.JWTAuth, nonAuthenticatedAPIs map[string][]string) func(http.Handler) http.Handler {
	return Authenticate(ja, nonAuthenticatedAPIs)
}
func Authenticate(ja *jwtauth.JWTAuth, nonAuthenticatedAPIs map[string][]string) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		hfn := func(w http.ResponseWriter, r *http.Request) {
			// Bypass authentication for allow-listed methods
			methods, ok := nonAuthenticatedAPIs[r.URL.Path]
			if ok {
				for _, m := range methods {
					if m == r.Method {
						next.ServeHTTP(w, r)
						return
					}
				}
			}

			bearer := r.Header.Get("Authorization")

			if bearer == "" {
				http.Error(w, "Unauthorized", http.StatusUnauthorized)
				return
			}

			var jwtString string
			if len(bearer) > 7 && strings.ToUpper(bearer[0:6]) == "BEARER" {
				jwtString = bearer[7:]
			} else {
				jwtString = bearer
			}

			log.Info().Msg("Jawt: " + jwtString)

			token, err := ja.Decode(jwtString)

			if err != nil {
				http.Error(w, err.Error(), http.StatusUnauthorized)
				return
			}

			if token == nil || jwt.Validate(token) != nil {
				http.Error(w, http.StatusText(http.StatusUnauthorized), http.StatusUnauthorized)
				return
			}

			claims, err := token.AsMap(context.Background())

			if err != nil {
				http.Error(w, err.Error(), http.StatusUnauthorized)
				return
			}

			userID := uint64(claims["user_id"].(float64))

			ctx := context.WithValue(r.Context(), "user_id", userID)

			// Token is authenticated, pass it through
			next.ServeHTTP(w, r.WithContext(ctx))
		}
		return http.HandlerFunc(hfn)
	}
}

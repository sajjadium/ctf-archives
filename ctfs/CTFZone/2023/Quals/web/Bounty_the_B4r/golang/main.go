package main

import (
	"net/http"
	"os"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/go-chi/jwtauth/v5"

	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
	"github.com/val1d/bb_ctf/api"
	"github.com/val1d/bb_ctf/controller"
	"github.com/val1d/bb_ctf/db"
)

func main() {

	log.Logger = zerolog.New(os.Stdout).With().Timestamp().Caller().Logger()
	database, err := db.Connect()

	if os.Getenv("JWT_SECRET") != "" {
		api.JwtSecret = os.Getenv("JWT_SECRET")
	} else {
		log.Fatal().Msg("No JWT secret provided")
	}

	var flag string
	if os.Getenv("FLAG") != "" {
		flag = os.Getenv("FLAG")
	} else {
		log.Fatal().Msg("No flag provided")
	}

	if err != nil {
		if err != nil {
			log.Fatal().
				Msg(err.Error())
		}
	}

	r := chi.NewRouter()
	r.Use(middleware.Logger)

	// Authentication
	tokenAuth := jwtauth.New("HS256", []byte(api.JwtSecret), nil)
	// Non-authenticated APIs (the login endpoint, for instance)
	nonAuthenticatedAPIs := map[string][]string{
		"/api/user/login":    {"POST"},
		"/api/user/register": {"POST"},
	}
	r.Use(api.Authenticator(tokenAuth, nonAuthenticatedAPIs))

	s := api.ServerInterface(controller.NewServer(*database))
	h := api.HandlerFromMuxWithBaseURL(s, r, "/api")
	database.Impl.AutoMigrate(&db.Users{}, &db.Report{}, &db.BBProgram{}, &db.ProgramMembers{})

	err = database.InitFlagReport(flag)
	if err != nil {
		log.Fatal().Msgf("error creating the secret report: %v", err)
	}

	err = database.InitPublicPrograms()
	if err != nil {
		log.Fatal().Msgf("error creating the public bb programs: %v", err)
	}

	log.Info().
		Msg("Running server")

	http.ListenAndServe(":3000", h)
}

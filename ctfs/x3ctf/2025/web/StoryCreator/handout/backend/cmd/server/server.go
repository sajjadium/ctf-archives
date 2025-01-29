package main

import (
	"context"
	"errors"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"

	"github.com/99designs/gqlgen/graphql/handler"
	"github.com/99designs/gqlgen/graphql/handler/extension"
	"github.com/99designs/gqlgen/graphql/handler/transport"
	"github.com/99designs/gqlgen/graphql/playground"
	"github.com/boxmein/cwte2024-chall/internal/exporter"
	"github.com/boxmein/cwte2024-chall/pkg/apq"
	"github.com/boxmein/cwte2024-chall/pkg/db"
	"github.com/boxmein/cwte2024-chall/pkg/flagcookie"
	"github.com/boxmein/cwte2024-chall/pkg/graph"
	"github.com/boxmein/cwte2024-chall/pkg/render"
	"github.com/boxmein/cwte2024-chall/pkg/repository/exports"
	"github.com/boxmein/cwte2024-chall/pkg/repository/images"
	"github.com/boxmein/cwte2024-chall/pkg/repository/stories"
	"github.com/boxmein/cwte2024-chall/pkg/tenant"
	"github.com/gin-contrib/static"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

const defaultPort = "8080"

func main() {
	ctx := context.Background()
	// Load flag
	flag := os.Getenv("FLAG")
	if flag == "" {
		log.Fatal("FLAG environment variable is required")
	}

	// Set up database
	databaseUrl := os.Getenv("DATABASE_URL")
	if databaseUrl == "" {
		log.Fatal("DATABASE_URL environment variable is required")
	}

	// db, err := db.GetSqlite()
	db, err := db.GetPostgres(ctx, databaseUrl)
	if err != nil {
		log.Fatal(fmt.Errorf("failed to open sqlite foo.db: %w", err))
	}
	defer db.Close()
	log.Println("Database has been opened")

	// Set up repositories
	storiesRepository := stories.New(db)
	imagesRepository := images.New(db)
	exportsRepository := exports.New(db)

	// Set up GraphQL API
	cache := apq.NewAPQCache()
	resolver := graph.Resolver{
		DB: graph.ResolverDB{
			Stories: storiesRepository,
			Images:  imagesRepository,
			Exports: exportsRepository,
		},
	}
	config := graph.Config{Resolvers: &resolver}
	schema := graph.NewExecutableSchema(config)
	srv := handler.New(schema)
	srv.AddTransport(transport.POST{})
	srv.AddTransport(transport.MultipartForm{}) // Uploads
	srv.Use(extension.Introspection{})
	srv.Use(extension.FixedComplexityLimit(100))
	srv.Use(extension.AutomaticPersistedQuery{
		Cache: cache,
	})

	// Set up HTTP server
	router := gin.Default()

	router.Use(static.Serve("/", static.LocalFile(os.Getenv("FRONTEND_DIST"), true)))
	router.NoRoute(func(c *gin.Context) {
		// render same as index.html
		c.File(os.Getenv("FRONTEND_DIST") + "/index.html")
	})

	router.Use(TenantIDMiddleware())
	router.Use(FlagCookieMiddleware())

	group := router.Group("/api")

	hnd := playground.Handler("GraphQL playground", "/api/graphql")
	group.GET("/", func(c *gin.Context) {
		hnd.ServeHTTP(c.Writer, c.Request)
	})

	group.GET("/images/:id", func(c *gin.Context) {

		tenantID := c.MustGet("tenantID").(string)

		id, err := strconv.Atoi(c.Param("id"))
		if err != nil {
			c.JSON(400, gin.H{"error": "invalid image ID"})
		}
		imageBytes, err := imagesRepository.GetImage(ctx, tenantID, int64(id))
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		c.Data(http.StatusOK, "image/png", imageBytes)
	})

	group.GET("/export/:id", func(c *gin.Context) {
		tenantID := c.MustGet("tenantID").(string)
		id, err := strconv.Atoi(c.Param("id"))
		if err != nil {
			c.JSON(400, gin.H{"error": "invalid image ID"})
		}
		imageBytes, err := exportsRepository.GetExportImage(ctx, tenantID, int64(id))
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		c.Data(http.StatusOK, "image/png", imageBytes)
	})

	group.POST("/graphql", func(c *gin.Context) {
		srv.ServeHTTP(c.Writer, c.Request)
	})

	port := os.Getenv("PORT")
	if port == "" {
		port = defaultPort
	}

	frontendURL := fmt.Sprintf("http://localhost:%s", port)

	// Set up exporter
	renderer := render.NewRenderer(frontendURL, flag)
	exporter := exporter.New(exportsRepository, renderer)
	exporterCtx, cancel := context.WithCancel(ctx)
	defer cancel()
	go func() {
		err := exporter.Run(exporterCtx)
		if err != nil {
			log.Printf("exporter failed: %v",
				err)
		}
	}()

	// Start listening

	log.Printf("connect to %s for GraphQL playground", frontendURL)
	router.Run(":" + port)
}

// cheap way to isolate data between players
func TenantIDMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		tenantID := ""
		if tenantIDCookie, err := c.Cookie("tenantID"); errors.Is(err, http.ErrNoCookie) {
			if generatedID, err := uuid.NewRandom(); err != nil {
				c.AbortWithStatusJSON(http.StatusInternalServerError, gin.H{"error": "failed to generate tenant ID"})
				return
			} else {
				tenantID = generatedID.String()
				c.SetCookie("tenantID", tenantID, 0, "/", "", false, false)
			}
		} else {
			tenantID = tenantIDCookie
		}
		c.Request = c.Request.WithContext(
			tenant.SetTenantID(c.Request.Context(), tenantID),
		)
		c.Set("tenantID", tenantID)
	}
}

func FlagCookieMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		flagCookieHeader, err := c.Cookie("flag")
		if err != nil {
			flagCookieHeader = ""
		}
		newCtx := flagcookie.SetFlagCookie(c.Request.Context(), flagCookieHeader)
		c.Request = c.Request.WithContext(newCtx)
	}
}

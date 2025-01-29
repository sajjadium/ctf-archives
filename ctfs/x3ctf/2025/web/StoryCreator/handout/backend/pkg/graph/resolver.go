package graph

import (
	"github.com/boxmein/cwte2024-chall/pkg/repository/exports"
	"github.com/boxmein/cwte2024-chall/pkg/repository/images"
	"github.com/boxmein/cwte2024-chall/pkg/repository/stories"
)

//go:generate go run github.com/99designs/gqlgen generate

// This file will not be regenerated automatically.
//
// It serves as dependency injection for your app, add any dependencies you require here.

type ResolverDB struct {
	Stories stories.StoriesRepository
	Images  images.ImagesRepository
	Exports exports.ExportsRepository
}

type Resolver struct {
	DB ResolverDB
}

package apq

import (
	"context"

	"github.com/99designs/gqlgen/graphql"
	"github.com/boxmein/cwte2024-chall/pkg/smallhmap"
	"github.com/boxmein/cwte2024-chall/pkg/tenant"
)

type APQCache struct {
	queries smallhmap.SmallHmap
}

// Add implements graphql.Cache.
func (a *APQCache) Add(ctx context.Context, key string, value any) {
	t := tenant.GetTenantID(ctx)
	key = t + key
	a.queries.Add(ctx, key, value)
}

// Get implements graphql.Cache.
func (a *APQCache) Get(ctx context.Context, key string) (value any, ok bool) {
	t := tenant.GetTenantID(ctx)
	key = t + key
	return a.queries.Get(ctx, key)
}

var _ graphql.Cache = (*APQCache)(nil)

func NewAPQCache() graphql.Cache {
	return &APQCache{queries: smallhmap.New()}
}

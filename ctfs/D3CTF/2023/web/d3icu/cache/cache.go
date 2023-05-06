package main

import (
	"context"
	"github.com/go-redis/redis/v8"
	"time"
)

type Cache struct {
	client *redis.Client
}

func (c Cache) Set(ctx context.Context, key string, value []byte, expire time.Duration) error {
	return c.client.Set(ctx, key, value, expire).Err()
}

func (c Cache) Get(ctx context.Context, key string) ([]byte, error) {
	return c.client.Get(ctx, key).Bytes()
}

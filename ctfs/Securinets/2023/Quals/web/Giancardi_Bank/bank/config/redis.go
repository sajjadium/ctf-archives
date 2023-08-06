package config

import (
	"fmt"
	"log"
	"os"
	"time"

	"github.com/go-redis/redis/v8"
)

type IRedisConnection interface {
	close() error
}

type RedisConnection struct {
	client *redis.Client
}

var Cache RedisConnection

func MustInitCache(dbkey int) error {

	redisClient := redis.NewClient(&redis.Options{
		Addr: os.Getenv("REDIS_HOST"),
		DB:   dbkey,
	})

	// Test the Redis connection
	pong, err := redisClient.Ping(redisClient.Context()).Result()
	if err != nil {
		log.Fatalf("Could not connect to Redis: %v", err)
		panic(err)
	}
	fmt.Println("Connected to Redis:", pong)

	Cache = RedisConnection{
		client: redisClient,
	}
	return nil
}

func (r RedisConnection) Close() error {
	return r.client.Close()
}

func (r RedisConnection) Get(key string) (string, error) {
	return r.client.Get(r.client.Context(), key).Result()
}

func (r RedisConnection) Set(key string, value string) error {
	return r.client.Set(r.client.Context(), key, value, 30*time.Second).Err()
}

package smallhmap

import (
	"context"
	"log"
)

type SmallHmap interface {
	Add(ctx context.Context, key string, value any)
	Get(ctx context.Context, key string) (value any, ok bool)
}

const MAX_SIZE = 5000

// Constant size O(1) hash map
// Uses short keys for optimized performance
// Optimized for web
type smallHmap struct {
	queries map[uint64]any
}

// Add implements SmallHmap.
func (s *smallHmap) Add(ctx context.Context, key string, value any) {
	smallKey := makeKeySmaller(key)
	s.queries[smallKey] = value
}

// Get implements SmallHmap.
func (s *smallHmap) Get(ctx context.Context, key string) (value any, ok bool) {
	smallKey := makeKeySmaller(key)
	res := s.queries[smallKey]

	if res == nil {
		return nil, false
	}
	if res, ok := res.(string); ok && res == "" {
		log.Printf("empty string for key %s", key)
		return nil, false
	}
	return res, true
}

func New() SmallHmap {
	return &smallHmap{queries: make(map[uint64]any)}
}

func makeKeySmaller(key string) uint64 {
	sum := uint64(0)
	for _, c := range key {
		sum += uint64(c)
	}
	return sum % MAX_SIZE
}

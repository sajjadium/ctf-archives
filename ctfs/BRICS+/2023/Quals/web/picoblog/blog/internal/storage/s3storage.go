package storage

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"time"

	"github.com/minio/minio-go/v7"
	"github.com/minio/minio-go/v7/pkg/credentials"
)

const (
	requestTimeout = time.Second * 5
	maxObjectSize  = 1 << 14
	jsonFileExt    = ".json"
)

var (
	// ErrTooLarge is returned to avoid saving huge objects and wasting space on the S3 storage.
	ErrTooLarge = errors.New("object to save is too large")

	// ErrTooLarge is returned when an object doesn't exist on the S3 Storage.
	ErrNotExists = errors.New("object doesn't exist")
)

// S3Storage provides a blog storage based on an Amazon S3 object storage.
type S3Storage struct {
	client *minio.Client
	bucket string
}

// NewS3Storage initializes a new S3-based storage and checks that the specified bucket exists.
func NewS3Storage(endpoint, accessKeyID, secretAccessKey, bucket string) (*S3Storage, error) {
	client, err := minio.New(endpoint, &minio.Options{
		BucketLookup: minio.BucketLookupPath,
		Creds:        credentials.NewStaticV4(accessKeyID, secretAccessKey, ""),
		Secure:       true,
	})
	if err != nil {
		return nil, fmt.Errorf("initializing S3 client: %w", err)
	}

	ctx, cancel := context.WithTimeout(context.Background(), requestTimeout)
	defer cancel()

	if ok, err := client.BucketExists(ctx, bucket); err != nil {
		return nil, fmt.Errorf("verifying that bucket %q exists: %w", bucket, err)
	} else if !ok {
		return nil, fmt.Errorf("bucket %q doesn't exist in S3", bucket)
	}

	return &S3Storage{
		client: client,
		bucket: bucket,
	}, nil
}

// SaveBlog saves a blog object to the storage.
func (s *S3Storage) SaveBlog(ctx context.Context, b *Blog) error {
	data, err := json.Marshal(b)
	if err != nil {
		return fmt.Errorf("marshaling blog object: %w", err)
	}

	return s.saveObject(ctx, b.ID, data)
}

// GetBlog gets a blog object by its ID from the storage.
func (s *S3Storage) GetBlog(ctx context.Context, blogID string) (*Blog, error) {
	data, err := s.getObject(ctx, blogID)
	if err != nil {
		return nil, err
	}

	b := new(Blog)

	if err := json.Unmarshal(data, b); err != nil {
		return nil, fmt.Errorf("unmarshaling blog object: %w", err)
	}

	b.ID = blogID

	return b, nil
}

func (s *S3Storage) saveObject(ctx context.Context, key string, data []byte) error {
	if len(data) > maxObjectSize {
		return ErrTooLarge
	}

	ctx, cancel := context.WithTimeout(ctx, requestTimeout)
	defer cancel()

	_, err := s.client.PutObject(ctx, s.bucket, key+jsonFileExt, bytes.NewReader(data), int64(len(data)), minio.PutObjectOptions{
		ContentType: "application/json",
	})
	if err != nil {
		return fmt.Errorf("saving object %q to storage: %w", key, err)
	}

	return nil
}

func (s *S3Storage) getObject(ctx context.Context, key string) ([]byte, error) {
	ctx, cancel := context.WithTimeout(ctx, requestTimeout)
	defer cancel()

	object, err := s.client.GetObject(ctx, s.bucket, key+jsonFileExt, minio.GetObjectOptions{})
	if err != nil {
		resp := minio.ToErrorResponse(err)
		if resp.StatusCode == http.StatusNotFound {
			return nil, err
		}

		return nil, fmt.Errorf("getting object %q from storage: %w", key, err)
	}

	defer object.Close()

	data, err := io.ReadAll(object)
	if err != nil {
		return nil, fmt.Errorf("reading object %q data: %w", key, err)
	}

	return data, nil
}

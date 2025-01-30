package images

import (
	"context"
	"database/sql"
)

type Image struct {
	ID    int64
	Image []byte
}

type ImagesRepository interface {
	ListImageIDs(ctx context.Context, tenantID string) ([]int64, error)
	SaveImage(ctx context.Context, tenantID string, image []byte) (int64, error)
	GetImage(ctx context.Context, tenantID string, id int64) ([]byte, error)
}

type imagesRepository struct {
	db *sql.DB
}

func (r *imagesRepository) SaveImage(ctx context.Context, tenantID string, image []byte) (int64, error) {
	var id int64
	err := r.db.QueryRowContext(ctx, "INSERT INTO images (tenant_id, image) VALUES ($1, $2) RETURNING id", tenantID, image).Scan(&id)
	if err != nil {
		return -1, err
	}
	return id, nil
}

func (r *imagesRepository) GetImage(ctx context.Context, tenantID string, id int64) ([]byte, error) {
	var image []byte
	err := r.db.QueryRowContext(ctx, "SELECT image FROM images WHERE id = $1", id).Scan(&image)
	if err != nil {
		return nil, err
	}
	return image, nil
}

func (r *imagesRepository) ListImageIDs(ctx context.Context, tenantID string) ([]int64, error) {
	rows, err := r.db.QueryContext(ctx, "SELECT id FROM images")
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var ids []int64
	for rows.Next() {
		var id int64
		if err := rows.Scan(&id); err != nil {
			return nil, err
		}
		ids = append(ids, id)
	}
	return ids, nil
}

func New(db *sql.DB) ImagesRepository {
	return &imagesRepository{db: db}
}

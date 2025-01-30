package exports

import (
	"context"
	"database/sql"
	"fmt"

	"github.com/boxmein/cwte2024-chall/pkg/model"
)

type Export struct {
	ID         int64
	TenantID   string
	StoryID    int64
	Dimensions model.Dimensions
	Progress   string
	Ready      bool
	Image      []byte
}

type ExportsRepository interface {
	NewExport(ctx context.Context, tenantID string, export Export) (int64, error)
	GetExport(ctx context.Context, tenantID string, id int64) (*Export, error)
	GetExportImage(ctx context.Context, tenantID string, id int64) ([]byte, error)
	GetAllExports(ctx context.Context, tenantID string) ([]*Export, error)
	// for exporter
	GetIncompleteExports(ctx context.Context) ([]*Export, error)
	UpdateExportStatus(ctx context.Context, id int64, status string) error
	MarkExportReady(ctx context.Context, id int64, image []byte) error
}

type exportsRepository struct {
	db *sql.DB
}

func (e *exportsRepository) GetExportImage(ctx context.Context, tenantID string, id int64) ([]byte, error) {
	var image []byte
	err := e.db.QueryRowContext(ctx, "SELECT image FROM exports WHERE id = $1", id).Scan(&image)
	if err != nil {
		return nil, fmt.Errorf("failed to get export image: %w", err)
	}
	return image, nil
}

func (e *exportsRepository) GetAllExports(ctx context.Context, tenantID string) ([]*Export, error) {
	rows, err := e.db.QueryContext(ctx, "SELECT id, story_id, dimensions, progress, ready FROM exports")
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var exports []*Export
	for rows.Next() {
		var export Export
		if err := rows.Scan(&export.ID, &export.StoryID, &export.Dimensions, &export.Progress, &export.Ready); err != nil {
			return nil, err
		}
		exports = append(exports, &export)
	}
	return exports, nil
}

func (e *exportsRepository) GetIncompleteExports(ctx context.Context) ([]*Export, error) {
	rows, err := e.db.QueryContext(ctx, "SELECT id, story_id, dimensions, progress, ready, tenant_id FROM exports WHERE ready = false")
	if err != nil {
		return nil, fmt.Errorf("failed to get incomplete exports: %w", err)
	}
	defer rows.Close()

	var exports []*Export
	for rows.Next() {
		var row Export
		if err := rows.Scan(&row.ID, &row.StoryID, &row.Dimensions, &row.Progress, &row.Ready, &row.TenantID); err != nil {
			return nil, fmt.Errorf("failed to scan export row: %w", err)
		}
		exports = append(exports, &row)
	}
	return exports, nil
}

func (e *exportsRepository) MarkExportReady(ctx context.Context, id int64, image []byte) error {
	_, err := e.db.ExecContext(ctx, "UPDATE exports SET ready = true, progress = 'completed', image = $1 WHERE id = $2", image, id)
	if err != nil {
		return fmt.Errorf("failed to mark export ready: %w", err)
	}
	return nil
}

func (e *exportsRepository) UpdateExportStatus(ctx context.Context, id int64, status string) error {
	_, err := e.db.ExecContext(ctx, "UPDATE exports SET progress = $1 WHERE id = $2", status, id)
	if err != nil {
		return fmt.Errorf("failed to update export status: %w", err)
	}
	return nil
}

func (e *exportsRepository) GetExport(ctx context.Context, tenantID string, id int64) (*Export, error) {
	var row Export
	err := e.db.QueryRowContext(ctx, "SELECT id, story_id, dimensions, progress, ready FROM exports WHERE id = $1", id).Scan(&row.ID, &row.StoryID, &row.Dimensions, &row.Progress, &row.Ready)
	if err != nil {
		return nil, err
	}
	return &row, nil
}

func (e *exportsRepository) NewExport(ctx context.Context, tenantID string, export Export) (int64, error) {
	var id int64
	err := e.db.QueryRowContext(ctx, "INSERT INTO exports (story_id, dimensions, progress, ready, tenant_id) VALUES ($1, $2, $3, $4, $5) RETURNING id", export.StoryID, export.Dimensions, "queued", false, tenantID).Scan(&id)
	if err != nil {
		return -1, err
	}
	return id, nil
}

func New(db *sql.DB) ExportsRepository {
	return &exportsRepository{db: db}
}

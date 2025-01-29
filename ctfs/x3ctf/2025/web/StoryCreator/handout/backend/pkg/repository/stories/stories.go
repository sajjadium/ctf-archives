package stories

import (
	"context"
	"database/sql"
)

type Story struct {
	ID      int64
	Text    string
	Action  string
	ImageID int64
}

type StoriesRepository interface {
	NewStory(ctx context.Context, tenantID string, story Story) (int64, error)
	GetStory(ctx context.Context, tenantID string, id int64) (*Story, error)
	GetAllStories(ctx context.Context, tenantID string) ([]*Story, error)
}

type storiesRepository struct {
	db *sql.DB
}

func (s *storiesRepository) GetStory(ctx context.Context, tenantID string, id int64) (*Story, error) {
	var story Story
	err := s.db.QueryRowContext(ctx, "SELECT id, text, action, image_id FROM stories WHERE id = $1 LIMIT 1", id).Scan(&story.ID, &story.Text, &story.Action, &story.ImageID)
	if err == sql.ErrNoRows {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	return &story, nil
}

func (s *storiesRepository) NewStory(ctx context.Context, tenantID string, story Story) (int64, error) {
	var id int64
	err := s.db.QueryRowContext(ctx, "INSERT INTO stories (text, action, image_id, tenant_id) VALUES ($1, $2, $3, $4) RETURNING id", story.Text, story.Action, story.ImageID, tenantID).Scan(&id)
	if err != nil {
		return -1, err
	}
	return id, nil
}

func (s *storiesRepository) GetAllStories(ctx context.Context, tenantID string) ([]*Story, error) {
	rows, err := s.db.QueryContext(ctx, "SELECT id, text, action, image_id FROM stories")
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var stories []*Story
	for rows.Next() {
		var story Story
		if err := rows.Scan(&story.ID, &story.Text, &story.Action, &story.ImageID); err != nil {
			return nil, err
		}
		stories = append(stories, &story)
	}
	return stories, nil
}

func New(db *sql.DB) StoriesRepository {
	return &storiesRepository{db: db}
}

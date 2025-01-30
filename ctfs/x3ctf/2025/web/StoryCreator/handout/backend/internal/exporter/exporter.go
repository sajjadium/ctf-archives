package exporter

import (
	"fmt"
	"log"
	"time"

	"context"

	"github.com/boxmein/cwte2024-chall/pkg/render"
	"github.com/boxmein/cwte2024-chall/pkg/repository/exports"
)

type Exporter interface {
	Run(ctx context.Context) error
}

func New(repository exports.ExportsRepository, renderer render.Renderer) Exporter {
	return &exporter{
		repository: repository,
		renderer:   renderer,
	}
}

type exporter struct {
	repository exports.ExportsRepository
	renderer   render.Renderer
}

func (e *exporter) Run(ctx context.Context) error {
	for {
		err := e.runOneIteration(ctx)
		if err != nil {
			log.Printf("failed to run exporter, trying again later: %v", err)
		}
		time.Sleep(30 * time.Second)
	}
}

func (e *exporter) runOneIteration(ctx context.Context) error {
	exports, err := e.repository.GetIncompleteExports(ctx)
	if err != nil {
		return fmt.Errorf("failed to load incomplete exports: %w", err)
	}

	if len(exports) == 0 {
		return nil
	}

	log.Printf("Exporting %d stories", len(exports))
	err = e.runExports(ctx, exports)
	if err != nil {
		return fmt.Errorf("error completing exports: %w", err)
	}
	return nil
}

func (e *exporter) runExports(ctx context.Context, exports []*exports.Export) error {
	for _, export := range exports {
		err := e.runExport(ctx, *export)
		if err != nil {
			log.Printf("export ID %d failed: %v", export.ID, err)
			return fmt.Errorf("failed to run export ID %d: %w", export.ID, err)
		}
		log.Printf("export ID %d completed successfully", export.ID)
	}
	return nil
}

func (e *exporter) runExport(ctx context.Context, export exports.Export) error {
	ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
	defer cancel()
	if err := e.repository.UpdateExportStatus(ctx, export.ID, "task picked up"); err != nil {
		return fmt.Errorf("failed to update export status: %w", err)
	}
	img, err := e.renderer.RenderStory(ctx, export.TenantID, export.StoryID)
	if err != nil {
		if err := e.repository.UpdateExportStatus(ctx, export.ID, "failed to render story to image"); err != nil {
			return fmt.Errorf("failed to update export status: %w", err)
		}
		return fmt.Errorf("failed to render story to image: %w", err)
	}
	if err := e.repository.MarkExportReady(ctx, export.ID, img); err != nil {
		return fmt.Errorf("failed to mark export ready: %w", err)
	}
	return nil
}

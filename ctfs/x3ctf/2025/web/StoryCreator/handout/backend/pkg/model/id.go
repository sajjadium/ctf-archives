package model

import "fmt"

// ID is a newtype that represents an ID. It is just a string
type ID string

func ConvertToID(integerId int64) ID {
	return ID(fmt.Sprintf("%d", integerId))
}

// ID is a newtype that represents an ID. It is just a string
type StoryID string

func ConvertToStoryID(integerId int64) StoryID {
	return StoryID(fmt.Sprintf("%d", integerId))
}

// ID is a newtype that represents an ID. It is just a string
type ImageID string

func ConvertToImageID(integerId int64) ImageID {
	return ImageID(fmt.Sprintf("%d", integerId))
}

// ID is a newtype that represents an ID. It is just a string
type ExportID string

func ConvertToExportID(integerId int64) ExportID {
	return ExportID(fmt.Sprintf("%d", integerId))
}

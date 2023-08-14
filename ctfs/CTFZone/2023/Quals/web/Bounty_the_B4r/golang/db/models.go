package db

const (
	ProgramTypePublic = iota
	ProgramTypePrivate
)

type Users struct {
	ID         uint64 `gorm:"primaryKey"`
	Username   string
	Password   []byte
	Reputation uint64
	Pow        string
}

type Report struct {
	ID          uint64 `gorm:"primaryKey"`
	UUID        string
	Title       string
	Description string
	Program     string
	Severity    string
	Weakness    string
	Published   int64
	Reporter    uint64
}

type BBProgram struct {
	ID   string `gorm:"primaryKey"`
	Name string
	Type uint64 //0-public; 1-private
}

type ProgramMembers struct {
	ID        uint64 `gorm:"primaryKey"`
	ProgramID string
	UserID    uint64
}

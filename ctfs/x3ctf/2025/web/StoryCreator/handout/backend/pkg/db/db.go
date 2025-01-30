package db

import (
	"context"
	"database/sql"

	_ "github.com/jackc/pgx/v5/stdlib"

	_ "github.com/mattn/go-sqlite3"
)

func GetSqlite() (*sql.DB, error) {
	return sql.Open("sqlite3", "foo.db")
}

func GetPostgres(ctx context.Context, url string) (*sql.DB, error) {
	return sql.Open("pgx", url)
}

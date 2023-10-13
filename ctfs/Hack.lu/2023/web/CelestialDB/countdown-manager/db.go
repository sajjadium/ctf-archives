package main

import (
	"context"
	"log"
	"os"

	"github.com/jackc/pgx/v4"
	"github.com/jackc/pgx/v4/pgxpool"
)

func connectDb() *pgxpool.Pool {
	dbUrl := os.Getenv("DB_URL")
	if dbUrl == "" {
		dbUrl = "postgres://postgres:postgres@localhost:5432/countdown_manager"
	}

	// connection config
	config, err := pgxpool.ParseConfig(dbUrl)
	if err != nil {
		log.Fatalf("Unable to parse db URL: %v\n", err)
	}
	config.ConnConfig.PreferSimpleProtocol = true

	// connect
	db, err := pgxpool.ConnectConfig(context.Background(), config)
	if err != nil {
		log.Fatalf("Unable to connect to database: %v\n", err)
	}

	// create tables if they don't exist
	_, err = db.Query(context.Background(), `CREATE TABLE IF NOT EXISTS counters (
		id BIGSERIAL PRIMARY KEY,
		name TEXT NOT NULL,
		count BIGINT NOT NULL,
		created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
		created_by TEXT NOT NULL,
		updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
		updated_by TEXT
	);`)
	if err != nil {
		log.Fatalf("Create table failed: %v\n", err)
	}

	return db
}

func scanCounter(row pgx.Row) (Counter, error) {
	var counter Counter
	err := row.Scan(&counter.Id, &counter.Name, &counter.Count, &counter.CreatedAt, &counter.CreatedBy, &counter.UpdatedAt, &counter.UpdatedBy)
	return counter, err
}

func getAllCounters(db *pgxpool.Pool) ([]Counter, error) {
	rows, err := db.Query(context.Background(), "SELECT * FROM counters")
	if err != nil {
		log.Printf("Query failed: %v\n", err)
		return nil, err
	}
	defer rows.Close()
	var counters []Counter
	counters = make([]Counter, 0)
	for rows.Next() {
		counter, err := scanCounter(rows)
		if err != nil {
			log.Printf("Query failed: %v\n", err)
			return nil, err
		}
		counters = append(counters, counter)
	}
	return counters, nil
}

func createCounter(db *pgxpool.Pool, c CounterCreation) (Counter, error) {
	row := db.QueryRow(context.Background(), "INSERT INTO counters (name, count, created_by) VALUES ($1, $2, $3) RETURNING *", c.Name, c.Count, c.CreatedBy)
	return scanCounter(row)
}

func getCounter(db *pgxpool.Pool, id int64) (Counter, error) {
	row := db.QueryRow(context.Background(), "SELECT * FROM counters WHERE id=$1", id)
	return scanCounter(row)
}

func updateCounter(db *pgxpool.Pool, id int64, decrement int64, updatedBy string) (Counter, error) {
	row := db.QueryRow(context.Background(), "UPDATE counters SET count=count-$1, updated_by=$2 WHERE id=$3 RETURNING *", decrement, updatedBy, id)
	return scanCounter(row)
}

func deleteCounter(db *pgxpool.Pool, id int64) error {
	_, err := db.Exec(context.Background(), "DELETE FROM counters WHERE id=$1", id)
	return err
}

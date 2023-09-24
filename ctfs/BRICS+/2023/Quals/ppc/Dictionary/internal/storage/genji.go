package storage

import (
	"fmt"
	"strings"

	"github.com/genjidb/genji"
)

// Genji provides dictionary storage using the Genji DB.
type Genji struct {
	db *genji.DB
}

// OpenGenji opens the Genji DB at the specified directory path.
// After OpenGenji don't forget to execute defer db.Close() on the returned database.
func OpenGenji(path string) (*Genji, error) {
	db, err := genji.Open(path)
	if err != nil {
		return nil, fmt.Errorf("opening Genji: %w", err)
	}

	return &Genji{db: db}, nil
}

// Close closes the database and returns an error if one occurred.
func (g *Genji) Close() error {
	if err := g.db.Close(); err != nil {
		return fmt.Errorf("closing Genji: %w", err)
	}

	return nil
}

// Initialize initializes the database using the specified dictionary word
// and flag word loaders if it hasn't yet been initialized.
// A single transaction is used both for the creation and filling of tables,
// so a failure would cause everything to rollback.
func (g *Genji) Initialize(wordLoader func() []string, flagParts []string) error {
	err := g.db.Update(func(tx *genji.Tx) error {
		// Fast check to see if the DB is already initialized
		if ok, err := g.isInitialized(tx); err != nil {
			return err
		} else if ok {
			return nil
		}

		if err := g.createTable(tx, "dictionary", wordLoader()); err != nil {
			return err
		}

		if err := g.createTable(tx, "flag", flagParts); err != nil {
			return err
		}

		if err := g.markInitialized(tx); err != nil {
			return err
		}

		return nil
	})
	if err != nil {
		return fmt.Errorf("running update transaction: %w", err)
	}

	return nil
}

// WordExists checks if a given word exists in the dictionary with the specified index.
func (g *Genji) WordExists(word string) (bool, error) {
	query := fmt.Sprintf(`select word from dictionary where word = '%s'`, word)

	var found bool

	g.db.View(func(tx *genji.Tx) error {
		if _, err := tx.QueryDocument(query); genji.IsNotFoundError(err) {
			return nil
		} else if err != nil {
			return fmt.Errorf("executing WordExists query %q: %w", query, err)
		}

		found = true
		return nil
	})

	return found, nil
}

func (g *Genji) createTable(tx *genji.Tx, name string, words []string) error {
	createQuery := fmt.Sprintf(`
		create table %s (
			id int primary key,
			word text not null
		);

		create index %s_word_idx on %s (word);
	`, name, name, name)

	insertQuery := fmt.Sprintf(`
		insert into %s values (?, ?)
	`, name) + strings.Repeat(", (?, ?)", len(words)-1)

	if err := tx.Exec(createQuery); err != nil {
		return fmt.Errorf("creating table %s: %w", name, err)
	}

	args := make([]any, 0, len(words)*2)
	for i, word := range words {
		args = append(args, i, word)
	}

	if err := tx.Exec(insertQuery, args...); err != nil {
		return fmt.Errorf("inserting words into table %s: %w", name, err)
	}

	return nil
}

func (g *Genji) markInitialized(tx *genji.Tx) error {
	if err := tx.Exec(`create table init`); err != nil {
		return fmt.Errorf("marking as initialized: %w", err)
	}

	return nil
}

func (g *Genji) isInitialized(tx *genji.Tx) (bool, error) {
	if err := tx.Exec(`select 1 from init`); genji.IsNotFoundError(err) {
		return false, nil
	} else if err != nil {
		return false, fmt.Errorf("checking if DB is initialized: %w", err)
	}

	return true, nil
}

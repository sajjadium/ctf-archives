package main

import (
	"encoding/json"
	"net/http"

	"github.com/jackc/pgproto3/v2"
	"github.com/jackc/pgx/v4"
)

func positiveInt(n int64) int64 {
	if n < 0 {
		n = -n
	}
	return n
}

func rowToMap(rows pgx.Rows, fields []pgproto3.FieldDescription) map[string]interface{} {
	values, _ := rows.Values()
	rowJSON := make(map[string]interface{})
	for i := 0; i < len(fields); i++ {
		name := fields[i].Name
		value := values[i]
		rowJSON[string(name[:])] = value
	}
	return rowJSON
}

func rowsToJson(w http.ResponseWriter, rows pgx.Rows) error {
	if rows == nil {
		return nil
	}
	fields := rows.FieldDescriptions()
	resultsList := make([]map[string]interface{}, 0)
	for rows.Next() {
		resultsList = append(resultsList, rowToMap(rows, fields))
	}
	return json.NewEncoder(w).Encode(resultsList)
}

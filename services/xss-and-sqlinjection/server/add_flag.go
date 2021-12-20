package main

import (
	"database/sql"
	"net/http"
	"strings"
)

func addFlag(w http.ResponseWriter, r *http.Request) {
	vals := r.URL.Query()
	key := vals.Get("key")
	value := vals.Get("value")
	value = strings.Replace(value, "\"", "", -1)
	er := dbAddFlag(key, value)
	if er != nil {
		sendErrorAndLog(w, "Server error", er)
		return
	}
	sendSuccess(w)
}

func dbAddFlag(key, value string) error {
	q := "insert into [flag] ([key], [value]) values " +
		" (@key, @value);"
	_, er := db.Exec(q,
		sql.Named("key", key),
		sql.Named("value", value))
	return er
}

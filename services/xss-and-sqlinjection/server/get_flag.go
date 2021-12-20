package main

import (
	"database/sql"
	"errors"
	"net/http"
)

func getFlag(w http.ResponseWriter, r *http.Request) {
	vals := r.URL.Query()
	key := vals.Get("key")
	flag, er := dbGetFlag(key)
	if er != nil && er.Error() == "No flag" {
		sendJson(w, struct {
			NoFlag bool
		}{
			NoFlag: true,
		})
		return
	}
	if er != nil {
		sendErrorAndLog(w, "Server error", er)
		return
	}
	sendJson(w, struct {
		Value string
	}{
		Value: flag,
	})
}

func dbGetFlag(key string) (string, error) {
	q := "select top 1 [value] from [flag] where [key] = '" + key + "';"
	rows, er := db.Query(q)
	if er != nil {
		return "", er
	}
	defer rows.Close()
	if rows.Next() {
		var flag string
		er = rows.Scan(&flag)
		if er != nil {
			return "", er
		}
		return flag, nil
	}
	return "", errors.New("No flag")
}

func dbGetFlagSecure(key string) (string, error) {
	q := "select top 1 [value] from [flag] where [key] = @key;"
	rows, er := db.Query(q,
		sql.Named("key", key))
	if er != nil {
		return "", er
	}
	defer rows.Close()
	if rows.Next() {
		var flag string
		er = rows.Scan(&flag)
		if er != nil {
			return "", er
		}
		return flag, nil
	}
	return "", errors.New("No flag")
}

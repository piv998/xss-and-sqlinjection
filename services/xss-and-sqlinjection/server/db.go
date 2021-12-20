package main

import (
	"database/sql"
	"fmt"
	"log"
	"os"
	"strconv"
	"time"

	// we will use mssql server driver
	_ "github.com/denisenkom/go-mssqldb"
)

type dbConfig struct {
	Server string `json:"server"`
	Port   int    `json:"port"`
	User   string `json:"user"`
	Pass   string `json:"pass"`
}

// TimeToDB convert timeVal to string for MS SQL Server (DateTime2)
// milliseconds are not included
func TimeToDB(timeVal time.Time) string {
	return timeVal.UTC().Format("2006-01-02 15:04:05.0000000")
}

// TimeNullToDB convert timeVal to string for MS SQL Server (DateTime2)
// milliseconds are not included
// If timeVal is null, then "null" is returned
func TimeNullToDB(timeVal *time.Time) interface{} {
	if timeVal == nil {
		return nil
	}
	return timeVal.UTC().Format("2006-01-02 15:04:05.0000000")
}

// openDB opens MSSQL database with the name dbName
// Don't forget to close it with Close() invocation
func openDB(dbName string) *sql.DB {
	cfg := dbConfigFromEnv()
	var conStrTemplate string
	var conStr string
	if cfg.Port == 1433 {
		conStrTemplate = `server=%s;database=%s;user id=%s;password=%s;Connection Timeout=50000`
		conStr = fmt.Sprintf(conStrTemplate, cfg.Server, dbName, cfg.User, cfg.Pass)
	} else {
		conStrTemplate = `server=%s;port=%d;database=%s;user id=%s;password=%s;Connection Timeout=50000`
		conStr = fmt.Sprintf(conStrTemplate, cfg.Server, cfg.Port, dbName, cfg.User, cfg.Pass)
	}
	// if you use "mssql" instead of "sqlserver",
	// then sql.Named() will not work
	db, er := sql.Open("sqlserver", conStr)
	if er != nil {
		log.Fatal(er)
	}
	// test connection
	er = db.Ping()
	if er != nil {
		log.Fatal(er)
	}
	setStandardDBSettings(db)
	return db
}

func dbConfigFromEnv() *dbConfig {
	port, er := strconv.Atoi(os.Getenv("MSPORT"))
	if er != nil {
		fmt.Fprintln(os.Stderr, "$MSPORT should be number")
		panic(er)
	}
	return &dbConfig{
		Server: os.Getenv("MSHOST"),
		Port:   port,
		User:   os.Getenv("MSUSER"),
		Pass:   os.Getenv("MSPASS"),
	}
}

// setStandardDBSettings change settings for this db-instance for
// the best concurrent access
func setStandardDBSettings(db *sql.DB) {
	db.SetMaxOpenConns(100)
	db.SetMaxIdleConns(100)
	db.SetConnMaxLifetime(10 * time.Minute)
}

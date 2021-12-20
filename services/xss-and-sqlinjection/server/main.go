package main

import (
	"database/sql"
	"flag"
	"log"
	"net/http"
	"os"
	"strconv"

	"github.com/gorilla/mux"
)

var db *sql.DB

/*
Environment variables:
$MSHOST=localhost\SQLEXPRESS1 or localhost
$MSPORT=1433
$MSUSER=sa
$MSPASS=example
$MSDBNAME=vuln
*/

func main() {
	db = openDB(os.Getenv("MSDBNAME"))
	defer db.Close()
	var p int
	flag.IntVar(&p, "port", 5000, "server port")
	flag.Parse()
	r := mux.NewRouter()
	r.HandleFunc("/api/add_flag", addFlag).Methods("GET")
	r.HandleFunc("/api/get_flag", getFlag).Methods("GET")
	// staticDir := "../client/build"
	staticDir := "."
	r.PathPrefix("/").Handler(http.FileServer(http.Dir("./" + staticDir + "/")))
	http.Handle("/", r)
	log.Print("[info] Starting listening on port ", p, ", static dir is ", staticDir)
	log.Fatal(http.ListenAndServe("0.0.0.0:"+strconv.Itoa(p), r))
}

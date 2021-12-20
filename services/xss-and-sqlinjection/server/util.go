package main

import (
	"encoding/json"
	"log"
	"net/http"
	"runtime/debug"
)

func sendErrorAndLog(w http.ResponseWriter, erMsg string, er error) {
	sendError(w, erMsg)
	logEr(er)
}

func sendError(w http.ResponseWriter, erMsg string) {
	sendJson(w, struct {
		Error string
	}{
		Error: erMsg,
	})
}

func sendJson(w http.ResponseWriter, obj interface{}) {
	er := json.NewEncoder(w).Encode(obj)
	if er != nil {
		logEr(er)
	}
}

func logEr(er error) {
	if er != nil {
		log.Println("[error]", er)
		debug.PrintStack()
	}
}

func sendSuccess(w http.ResponseWriter) {
	sendJson(w, struct {
		Success bool
	}{
		true,
	})
}

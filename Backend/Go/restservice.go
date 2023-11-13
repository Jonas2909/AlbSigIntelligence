package main

import (
	"log"
	"net/http"
)

func main() {
	log.Println("Function main")

	RegisterRoutes()
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		log.Fatal(err)
	}
}

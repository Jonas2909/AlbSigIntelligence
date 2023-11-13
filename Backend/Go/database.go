package main

import (
	"fmt"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"log"
)

type UserCredentials struct {
	ID       int
	Username string
	Password string
}

func DBConnector() (*gorm.DB, error) {
	log.Println("Function DBConnector")

	connStr := "host=localhost user=postgres password=dev port=5432 sslmode=disable"
	db, err := gorm.Open(postgres.Open(connStr), &gorm.Config{})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Connected to the database")
	return db, nil
}

func GetAllUsersFromDB() (error, []UserCredentials) {
	log.Println("Function GetAllUsersFromDB")
	var userCredentials []UserCredentials

	db, err := DBConnector()
	if err != nil {
		return err, nil
	}

	db.Find(&userCredentials)
	return nil, userCredentials
}

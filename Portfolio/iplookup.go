package main

import (
	"io"
	"net/http"
)

func LookUpIP() string {
	resp, err := http.Get("https://ipv4.icanhazip.com/")
	if err != nil {
		return "Request Failed"
	}
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "Request Failed"
	}

	return string(body)
}

package main

import (
	"io/ioutil"
	"net/http"
)

func LookUpIP() string {
	resp, err := http.Get("https://ipv4.icanhazip.com/")
	if err != nil {
		return "Request Failed"
	}
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "Request Failed"
	}

	return string(body)
}

package main

import "math/rand"

var RandomQuotes = []string{
	"Holy Smokes!",
	"Holy Smokes! Michelle is a STRONNNNGGGGG LEVEL 3",
	"Asians are smart",
	"Asians like to buy big houses",
}

func ReturnRandomDevlinQuote() string {
	max := 3
	min := 0
	return RandomQuotes[rand.Intn(max-min)+min]
}

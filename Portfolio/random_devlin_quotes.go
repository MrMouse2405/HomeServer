package main

import "math/rand"

var RandomQuotes = []string{
	"Holy Smokes!",
	"Holy Smokes! Michelle is a STRONNNNGGGGG LEVEL 3",
	"Asians are smart",
	"Asians like to buy big houses.",
	"These 2 guys over here know what they're doing.",
	"If my daughter is half Asian and half white and Luke is white, what will be the ratio of ethnicity of their children be?",
	"Edward, Tristian, and Abdul are strong students. They dont need univeristy, university needs them.",
	"You are no where near smart enough to skip this class",
	"I have a Asian Wife and a Dog",
	"Universities Scroll down to application list until they find last names starting from W, and start accepting from there.",
	"Devlin teaching gender studies? Thats never going to happen guys!",
}

func ReturnRandomDevlinQuote() string {
	max := 10
	min := 0
	return RandomQuotes[rand.Intn(max-min)+min]
}

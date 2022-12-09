package main

import "github.com/gofiber/fiber/v2"

func main() {
	app := fiber.New()

	app.Get("/fun/icanhazip", func(c *fiber.Ctx) error {
		return c.SendString(LookUpIP())
	})

	app.Get("/fun/devlin", func(c *fiber.Ctx) error {
		return c.SendString(ReturnRandomDevlinQuote())
	})

	/*

		Listening

	*/

	app.Listen(":8000")
}

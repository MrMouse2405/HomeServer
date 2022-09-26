package main

import "github.com/gofiber/fiber/v2"

func main() {
	app := fiber.New()

	app.Get("/icanhazip", func(c *fiber.Ctx) error {
		return c.SendString(LookUpIP())
	})

	app.Get("/devlin", func(c *fiber.Ctx) error {
		return c.SendString(ReturnRandomDevlinQuote())
	})

	app.Listen(":8080")
}

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

	/*

		Cyber Security Lesson 1 Stuff

	*/

	app.Get("/jdl_key/:user/:password", func(c *fiber.Ctx) error {
		if c.Params("user") == "Rick-Astley" && c.Params("password") == "Never-Gonna-Give-you-up!-Never-Gonna-Let-you-down!" {
			return c.SendString("My Grandma Run Faster Than Your Code.")
		}
		return c.SendString("Failure, Just Like My Son.")
	})

	app.Get("/jdl_admin_lookup/:user/:key", func(c *fiber.Ctx) error {
		if c.Params("user") == "blitz" && c.Params("key") == "My-Grandma-Run-Faster-Than-Your-Code." {
			return c.SendString("Password:Cope")
		}
		return c.SendString("Failure, Just Like My Son.")
	})

	app.Get("/jdl_login/:user/:password", func(c *fiber.Ctx) error {
		if c.Params("user") == "blitz" && c.Params("password") == "Cope" {
			return c.SendString("joojle_blitz_home.html")
		}
		return c.SendString("Failure, Just Like My Son.")
	})

	/*

		Listening

	*/

	app.Listen(":8000")
}

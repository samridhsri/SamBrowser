package main

import (
	"embed" // Import the embed package
	"log"   // For better error logging

	"github.com/wailsapp/wails/v2"
	"github.com/wailsapp/wails/v2/pkg/options"
	"github.com/wailsapp/wails/v2/pkg/options/assetserver"
)

//go:embed frontend/dist
var assets embed.FS // This line tells Go to embed the frontend/dist directory

func main() {
	// Create an instance of the app structure
	app := NewApp() // NewApp is defined in app.go

	// Create application with options
	err := wails.Run(&options.App{
		Title:  "Study Browser",
		Width:  1200,
		Height: 800,
		AssetServer: &assetserver.Options{
			Assets: assets, // Use the embedded assets here
		},
		OnStartup: app.Startup,
		Bind:      []interface{}{app},
	})

	if err != nil {
		log.Fatal("Error:", err.Error()) // Use log.Fatal for critical errors
	}
}
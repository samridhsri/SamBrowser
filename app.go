package main

import (
	"context"
	"fmt"
	"github.com/wailsapp/wails/v2/pkg/runtime"
)

// App struct
// Combines fields from both main.go and app.go
// Exports all necessary methods for Wails
//
type App struct {
	ctx         context.Context
	studyActive bool
}

// NewApp creates a new App application struct
func NewApp() *App {
	return &App{}
}

// Startup is called when the app starts. The context is saved
// so we can call the runtime methods
func (a *App) Startup(ctx context.Context) {
	a.ctx = ctx
}

// ToggleStudyMode toggles the study mode and logs the action
func (a *App) ToggleStudyMode() bool {
	a.studyActive = !a.studyActive
	runtime.LogInfo(a.ctx, "Study mode toggled")
	return a.studyActive
}

// Greet returns a greeting for the given name
func (a *App) Greet(name string) string {
	return fmt.Sprintf("Hello %s, It's show time!", name)
}

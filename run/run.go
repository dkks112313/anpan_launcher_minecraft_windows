package main

import (
	"os/exec"
	"syscall"

	"golang.org/x/sys/windows"
)

func main() {
	cmd := exec.Command("./main.exe")

	cmd.SysProcAttr = &syscall.SysProcAttr{
		CreationFlags: windows.CREATE_NO_WINDOW,
	}

	err := cmd.Start()
	if err != nil {
		panic(err)
	}
}

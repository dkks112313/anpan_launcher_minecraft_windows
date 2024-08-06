package main

import (
	"os/exec"
	"syscall"

	"golang.org/x/sys/windows"
)

func main() {
	// Подготовка команды для запуска
	cmd := exec.Command("./main.exe")

	// Настройка атрибутов процесса для скрытия окна
	cmd.SysProcAttr = &syscall.SysProcAttr{
		CreationFlags: windows.CREATE_NO_WINDOW,
	}

	// Запуск команды
	err := cmd.Start()
	if err != nil {
		panic(err)
	}
}

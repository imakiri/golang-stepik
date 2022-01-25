package main

import "github.com/imakiri/golang-stepik/testlib"

// Экспериментальная реализация крос-языкового тестировщика,
// архитектура которого была описана Антоном
func main() {
	new(testlib.Main).Supervise()
}

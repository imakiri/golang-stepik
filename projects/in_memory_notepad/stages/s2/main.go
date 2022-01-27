package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	const size = 5
	var storage [size]string
	var index int
	var scanner = bufio.NewScanner(os.Stdin)
	var exe = true
	for exe {
		fmt.Print("Enter command and data: ")
		if !scanner.Scan() {
			return
		}

		var input = strings.SplitN(scanner.Text(), " ", 2)
		switch input[0] {
		case "exit":
			exe = false
			fmt.Print("[Info] Bye!\n")
		case "create":
			if index >= size {
				fmt.Print("[Error] Notepad is full\n")
				continue
			}
			storage[index] = input[1]
			index++
			fmt.Print("[OK] The note was successfully created\n")
		case "list":
			for i, v := range storage {
				if v != "" {
					fmt.Printf("[Info] %d: %s\n", i+1, v)
				}
			}
			continue
		case "clear":
			index = 0
			for i := range storage {
				storage[i] = ""
			}
			fmt.Print("[OK] All notes were successfully deleted\n")
		default:
			fmt.Println("[Error] Unknown command")
		}
	}
}

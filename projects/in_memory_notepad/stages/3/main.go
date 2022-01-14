package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	var scanner = bufio.NewScanner(os.Stdin)
	fmt.Print("Enter the maximum number of notes: ")
	if !scanner.Scan() {
		return
	}

	var size, err = strconv.Atoi(scanner.Text())
	if err != nil {
		fmt.Print(err)
		return
	}

	var storage = make([]string, size)
	var index int
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
			fmt.Print("Bye!\n")
		case "create":
			if index >= size {
				fmt.Print("[Error] The list of notes is full\n")
				continue
			}
			if len(input) < 2 {
				fmt.Print("[Error] The note cannot be empty\n")
				continue
			}

			var note = strings.TrimSpace(input[1])
			if note == "" {
				fmt.Print("[Error] The note cannot be empty\n")
				continue
			}

			storage[index] = note
			index++
			fmt.Print("[OK] The note was successfully created\n")
		case "list":
			for i, v := range storage {
				fmt.Printf("Index %d: %s\n", i, v)
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

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
			if input[1] == "" {
				fmt.Print("[Error] The note cannot be empty\n")
				continue
			}
			storage[index] = input[1]
			index++
			fmt.Print("[OK] The note was successfully created\n")
		case "list":
			for i, v := range storage {
				fmt.Printf("Index %d: %s\n", i, v)
			}
			continue
		case "update":
			var data = strings.SplitN(input[1], " ", 2)
			var i, err = strconv.Atoi(data[0])
			if err != nil {
				fmt.Printf("[Error] Invalid index: %s\n", data[0])
			} else if !(0 <= i && i < size) {
				fmt.Printf("[Error] Index %d is out of the boundary [0, %d)\n", i, size)
			} else if i > index {
				fmt.Println("[Error] There is nothing to update")
			} else if i <= index {
				storage[i] = data[1]
				fmt.Printf("[OK] The note at index %d was successfully updated\n", i)
			} else {
				fmt.Println("[Error] Internal error occurred")
			}
			continue
		case "delete":
			var i, err = strconv.Atoi(input[1])
			if err != nil {
				fmt.Printf("[Error] Invalid index: %s\n", input[1])
			} else if !(0 <= i && i < size) {
				fmt.Printf("[Error] Index %d is out of the boundary [0, %d)\n", i, size)
			} else if i < index {
				for j := i; j < index; j++ {
					storage[j] = storage[j+1]
				}
				storage[index] = ""
				index--
				fmt.Printf("[OK] The note at index %d was successfully deleted\n", i)
			} else if i >= index {
				fmt.Println("[Error] There is nothing to delete")
			} else {
				fmt.Println("[Error] Internal error occurred")
			}
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



package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func extractNote(input []string) (string, error) {
	if len(input) < 2 {
		return "", fmt.Errorf("[Error] Missing note argument\n")
	}

	var note = strings.TrimSpace(input[1])
	if note == "" {
		return "", fmt.Errorf("[Error] Missing note argument\n")
	}

	return note, nil
}

func extractIndex(index int, size int, input []string) (int, []string, error) {
	if len(input) < 2 {
		return 0, nil, fmt.Errorf("[Error] Missing position argument\n")
	}

	var data = strings.SplitN(input[1], " ", 2)
	var i, err = strconv.Atoi(data[0])
	switch {
	case err != nil:
	    var strIndex = strings.TrimSpace(data[0])
	    if strIndex == "" {
	        return 0, nil, fmt.Errorf("[Error] Missing position argument\n")
	    }
		return 0, nil, fmt.Errorf("[Error] Invalid position: %s\n", data[0])
	case !(0 <= i-1 && i-1 < size):
		return 0, nil, fmt.Errorf("[Error] Position %d is out of the boundary [1, %d]\n", i, size)
	case i-1 > index:
		return 0, nil, fmt.Errorf("[Error] There is nothing to update\n")
	case i-1 <= index:
		return i-1, data, nil
	default:
		return 0, nil, fmt.Errorf("[Error] Internal error occurred")
	}
}


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
		fmt.Print("\nEnter command and data: ")
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
			var note, err = extractNote(input)
			if err != nil {
				fmt.Print(err)
				continue
			}

			storage[index] = note
			index++
			fmt.Print("[OK] The note was successfully created\n")
		case "list":
		    var c int
			for i, v := range storage {
			    if v != "" {
			        c++
			        fmt.Printf("[Info] %d: %s\n", i+1, v)
			    }
			}
			if c == 0 {
			    fmt.Println("[Info] Notepad is empty")
			}
			continue
		case "update":
			var i, data, err = extractIndex(index, size, input)
			if err != nil {
				fmt.Print(err)
				continue
			}

			var note, e = extractNote(data)
			if e != nil {
				fmt.Print(e)
				continue
			}

			storage[i] = note
			fmt.Printf("[OK] The note at position %d was successfully updated\n", i+1)
		case "delete":
			var i, _ , err = extractIndex(index, size, input)
			if err != nil {
				fmt.Print(err)
				continue
			}

			for j := i; j < index; j++ {
				storage[j] = storage[j+1]
			}
			storage[index] = ""
			index--
			fmt.Printf("[OK] The note at position %d was successfully deleted\n", i+1)
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

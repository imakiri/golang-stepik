package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	var exe = true
	var scanner = bufio.NewScanner(os.Stdin)
	for exe {
		// 		fmt.Print("\n\n\nejrwsjrsykrEnter command and data: srfjhsfdjgrk\n\n\n\n")
		fmt.Print("Enter command and data: ")
		if !scanner.Scan() {
			return
		}

		var input = strings.SplitN(scanner.Text(), " ", 2)
		switch input[0] {
		case "exit":
			exe = false
			fmt.Print("Bye!\n")
		default:
			fmt.Println(input[0])
		}
	}
}

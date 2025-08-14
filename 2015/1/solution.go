package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	floor := 0
	firstNegative := -1

	reader := bufio.NewReader(os.Stdin)
	moves, _ := reader.ReadString('\n')

	for i, char := range moves {
		if char == '(' {
			floor++
		} else if char == ')' {
			floor--

			if floor < 0 && firstNegative == -1 {
				firstNegative = i
			}
		}
	}

	fmt.Println(floor)
	fmt.Println(firstNegative)
}

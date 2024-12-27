package main

import (
	"fmt"
	"os"
)

func generateNumbers(length int) []string {
	var numbers []string

	// Create a slice with the base-3 digits
	digits := []rune{'0', '1', '2'}

	// Generate all possible combinations
	generateHelper("", length, digits, &numbers)

	return numbers
}

func generateHelper(current string, length int, digits []rune, numbers *[]string) {
	if length == 0 {
		*numbers = append(*numbers, current)
		return
	}

	for _, digit := range digits {
		generateHelper(current+string(digit), length-1, digits, numbers)
	}
}

func writeToFile(filename string, lines []string) error {
	file, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer file.Close()

	for _, line := range lines {
		_, err := file.WriteString(line + "\n")
		if err != nil {
			return err
		}
	}

	return nil
}

func main() {
	length := 15
	result := generateNumbers(length)

	// Save the generated numbers to a file
	filename := "output.txt"
	err := writeToFile(filename, result)
	if err != nil {
		fmt.Println("Error writing to file:", err)
		return
	}

	fmt.Printf("Numbers successfully saved to %s\n", filename)
}

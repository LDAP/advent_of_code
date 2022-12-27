package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

func main() {
	data, err := ioutil.ReadFile("input.txt")
	if err != nil {
		fmt.Fprintf(os.Stderr, "%v\n", err)
		os.Exit(1)
	}

	blocks := strings.Split(string(data), "\n\n")
	max := 0
	for _, block := range blocks {
		numbers := strings.Split(block, "\n")
		sum := 0
		for _, number := range numbers {
			intNumber, err := strconv.Atoi(number)
			if err != nil {
				fmt.Fprintf(os.Stderr, "%v\n", err)
				os.Exit(1)
			}
			sum += intNumber
		}
		if sum > max {
			max = sum
		}
	}

	fmt.Print(max)
}

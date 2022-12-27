package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"sort"
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
	intBlocks := make([]int, len(blocks))
	for i, block := range blocks {
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
		intBlocks[i] = sum

	}

	sort.Ints(intBlocks)

	sum := 0
	for i := len(blocks) - 3; i < len(blocks); i++ {
		sum += intBlocks[i]
	}

	fmt.Print(sum)
}

// --- Part Two ---
// The grove coordinate values seem nonsensical. While you ponder the mysteries of Elf encryption, you suddenly remember the rest of the decryption routine you overheard back at camp.

// First, you need to apply the decryption key, 811589153. Multiply each number by the decryption key before you begin; this will produce the actual list of numbers to mix.

// Second, you need to mix the list of numbers ten times. The order in which the numbers are mixed does not change during mixing; the numbers are still moved in the order they appeared in the original, pre-mixed list. (So, if -3 appears fourth in the original list of numbers to mix, -3 will be the fourth number to move during each round of mixing.)

package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func index[C comparable](slice []C, o C) int {
	for i := 0; i < len(slice); i++ {
		if slice[i] == o {
			return i
		}
	}
	panic("No element found.")
}

func wrap(idx int, n int) int {
	return ((idx % n) + n) % n
}

func swap(idx1, idx2 int, slice [][2]int, indexes map[int]int) {
	idx1_wrapped := wrap(idx1, len(slice))
	idx2_wrapped := wrap(idx2, len(slice))

	indexes[slice[idx2_wrapped][1]] = idx1_wrapped
	indexes[slice[idx1_wrapped][1]] = idx2_wrapped

	slice[idx1_wrapped], slice[idx2_wrapped] = slice[idx2_wrapped], slice[idx1_wrapped]
}

func main() {
	file, _ := os.Open("input.txt")
	scanner := bufio.NewScanner(file)

	// READ
	coords := make([][2]int, 0, 5000)
	i := 0
	zero_index := 0
	indexes := make(map[int]int, 5000)
	for scanner.Scan() {
		line := scanner.Text()
		intValue, _ := strconv.Atoi(line)
		coords = append(coords, [2]int{intValue * 811589153, i})
		indexes[i] = i
		if intValue == 0 {
			zero_index = i
		}
		i++
	}

	// MIX
	for m := 0; m < 10; m++ {
		for i := 0; i < len(coords); i++ {
			idx := indexes[i]
			nMoves := coords[idx][0]

			nMoves = nMoves % (len(coords) - 1)

			if nMoves >= 0 {
				for j := idx + 1; j <= idx+nMoves; j++ {
					swap(j, j-1, coords, indexes)
				}
			} else {
				for j := idx; j > idx+nMoves; j-- {
					swap(j, j-1, coords, indexes)
				}
			}

		}
	}

	// CALC RESULT
	grove := 0
	zero := indexes[zero_index]
	for i := 1000; i <= 3000; i += 1000 {
		grove += coords[(i+zero)%len(coords)][0]
	}
	fmt.Println(grove)
}

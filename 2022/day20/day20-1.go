// --- Day 20: Grove Positioning System ---
// It's finally time to meet back up with the Elves. When you try to contact them, however, you get no reply. Perhaps you're out of range?

// You know they're headed to the grove where the star fruit grows, so if you can figure out where that is, you should be able to meet back up with them.

// Fortunately, your handheld device has a file (your puzzle input) that contains the grove's coordinates! Unfortunately, the file is encrypted - just in case the device were to fall into the wrong hands.

// Maybe you can decrypt it?

// When you were still back at the camp, you overheard some Elves talking about coordinate file encryption. The main operation involved in decrypting the file is called mixing.

// The encrypted file is a list of numbers. To mix the file, move each number forward or backward in the file a number of positions equal to the value of the number being moved. The list is circular, so moving a number off one end of the list wraps back around to the other end as if the ends were connected.

// For example, to move the 1 in a sequence like 4, 5, 6, 1, 7, 8, 9, the 1 moves one position forward: 4, 5, 6, 7, 1, 8, 9. To move the -2 in a sequence like 4, -2, 5, 6, 7, 8, 9, the -2 moves two positions backward, wrapping around: 4, 5, 6, 7, 8, -2, 9.

// The numbers should be moved in the order they originally appear in the encrypted file. Numbers moving around during the mixing process do not change the order in which the numbers are moved.

// Then, the grove coordinates can be found by looking at the 1000th, 2000th, and 3000th numbers after the value 0, wrapping around the list as necessary. In the above example, the 1000th number after 0 is 4, the 2000th is -3, and the 3000th is 2; adding these together produces 3.

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
		coords = append(coords, [2]int{intValue, i})
		indexes[i] = i
		if intValue == 0 {
			zero_index = i
		}
		i++
	}

	// MIX
	for i := 0; i < len(coords); i++ {
		idx := indexes[i]
		nMoves := coords[idx][0]

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

	// CALC RESULT
	grove := 0
	zero := indexes[zero_index]
	for i := 1000; i <= 3000; i += 1000 {
		grove += coords[(i+zero)%len(coords)][0]
	}
	fmt.Println(grove)
}

package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

const Minutes int = 24

type state struct {
	total_geodes int
	gen          [3]int
	res          [3]int
}

type robot struct {
	cost [3]int
}

type blueprint struct {
	robots [4]robot
}

func add_robots(s *state) state {
	new_res := [3]int{s.gen[0] + s.res[0], s.gen[1] + s.res[1], s.gen[2] + s.res[2]}
	return state{total_geodes: s.total_geodes, gen: s.gen, res: new_res}
}

func prune(geode int, m int, best_geode int) bool {
	for r := m; r <= Minutes; r++ {
		geode += Minutes - r - 1
	}
	return geode < best_geode
}

func can_buy(s *state, r *robot) bool {
	return r.cost[0] <= s.res[0] && r.cost[1] <= s.res[1] && r.cost[2] <= s.res[2]
}

func main() {
	file, _ := os.Open("input.txt")
	defer file.Close()

	scanner := bufio.NewScanner(file)
	bps := []blueprint{}
	for scanner.Scan() {
		line := strings.TrimRight(scanner.Text(), ".")

		bp := blueprint{}
		var idx int

		fmt.Sscanf(line,
			"Blueprint %d: Each ore robot costs %d ore. Each clay robot costs %d ore. Each obsidian robot costs %d ore and %d clay. Each geode robot costs %d ore and %d obsidian",
			&idx,
			&bp.robots[0].cost[0],
			&bp.robots[1].cost[0],
			&bp.robots[2].cost[0],
			&bp.robots[2].cost[1],
			&bp.robots[3].cost[0],
			&bp.robots[3].cost[2],
		)

		bps = append(bps, bp)

	}

	best_geodes := []int{}

	for i := 0; i < len(bps); i++ {
		fmt.Printf("%d / %d: ", i+1, len(bps))

		states := map[state]bool{{gen: [3]int{1, 0, 0}}: true}
		next_states := map[state]bool{}
		best_geode := 0

		for m := 0; m <= Minutes; m++ {
			fmt.Printf("%d ", m)

			for st := range states {
				if prune(st.total_geodes, m, best_geode) {
					continue
				}

				if !prune(st.total_geodes, m+1, best_geode) {
					(next_states)[add_robots(&st)] = true
				}

				for r := 0; r < len(bps[i].robots); r++ {
					if can_buy(&st, &bps[i].robots[r]) {
						next_st := st

						if r == 3 {
							next_st.total_geodes = st.total_geodes + (Minutes - m - 1)
						} else {
							next_st.total_geodes = st.total_geodes
							next_st.gen[r]++
						}

						if prune(next_st.total_geodes, m+1, best_geode) {
							continue
						}

						if next_st.total_geodes > best_geode {
							best_geode = next_st.total_geodes
						}

						for j := 0; j < 3; j++ {
							next_st.res[j] += st.gen[j]
							next_st.res[j] -= bps[i].robots[r].cost[j]
						}

						(next_states)[next_st] = true
					}
				}
			}

			states = next_states
			next_states = map[state]bool{}
		}

		best_geodes = append(best_geodes, best_geode)
		fmt.Println()
	}

	fmt.Println(best_geodes)
	value := 0
	for i, g := range best_geodes {
		value += (i + 1) * g
	}
	fmt.Println(value)
}

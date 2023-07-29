class Anagram:
    num_iterations = 0
    def anagram_expand(self, state, goal):
        node_list = []

        for pos in range(1, len(state)):  # Create each possible state that can be created from the current one in a single step
            new_state = state[1:pos + 1] + state[0] + state[pos + 1:]

            # TO DO: c. Very simple h' function - please improve!
            score = 0
            i = 0
            j = 0

            if new_state != goal:
                while new_state[i] == goal[j]:
                    score += 1
                    i += 1
                    j += 1

                while new_state[i] != goal[j]:
                    score += 1
                    i += 1
            
            node_list.append((new_state, score))

        return node_list

    # TO DO: b. Return either the solution as a list of states from start to goal or [] if there is no solution.
    def a_star(self, start, goal, expand):
        G = dict()
        OPEN = [(start, 0)]
        CLOSED = set()
        DISTANCE = {start: 0}

        while OPEN:
            n = OPEN[0][0]
            OPEN.remove(OPEN[0])

            if n in CLOSED:
                continue

            CLOSED.add(n)

            if n == goal:
                solution = [n]
                while n != start:
                    n = G[n]
                    solution.append(n)
                return list(reversed(solution))
            
            M = expand(n, goal)

            for m in M:
                neighbor = m[0]

                h_score = m[1]
                g_score = DISTANCE[n] + 1
                f_score = g_score + h_score

                OPEN.append((neighbor, f_score))

                if neighbor not in DISTANCE or g_score < DISTANCE[neighbor]:
                    DISTANCE[neighbor] = g_score
                    G[neighbor] = n

            OPEN.sort(key = lambda arr: arr[1])
            self.num_iterations += 1

        return []

    # Finds a solution, i.e., a placement of all rectangles within the given field, for a rectangle puzzle
    def solve(self,start, goal):

        self.num_iterations = 0

        # TO DO: a. Add code below to check in advance whether the problem is solvable

        if len(start) != len(goal):
            print('This is clearly impossible. I am not even trying to solve this.')
            return "IMPOSSIBLE"
        
        charCounter = [0] * 26
        for i in range(len(start)):
            c1 = start[i]
            c2 = goal[i]
            charCounter[ord(c1) - ord('A')] += 1
            charCounter[ord(c2) - ord('A')] -= 1
        
        for i in range(len(charCounter)):
            if charCounter[i] != 0:
                print('This is clearly impossible. I am not even trying to solve this.')
                return "IMPOSSIBLE"
        
        self.solution = self.a_star(start, goal, self.anagram_expand)

        if not self.solution:
            print('No solution found. This is weird, I should have caught this before even trying A*.')
            return "NONE"

        print(str(len(self.solution) - 1) + ' steps from start to goal:')

        for step in self.solution:
            print(step)

        print(str(self.num_iterations) + ' A* iterations were performed to find this solution.')

        return str(self.num_iterations)



if __name__ == '__main__':
    anagram = Anagram()
    anagram.solve('TRACE', 'CRATE')
    anagram.solve('PREDATOR', 'TEARDROP')


MRV = 1
FC = 2
AC3 = 3


class nQueens:

    def __init__(self, n, mrv=False,  inference=None):
        self.n = n
        self.assignment = [-1] * n  # each element is the row index for corresponding column, -1 means no assignment yet
        self.domain = [list(range(n)) for _ in range(n)] # available values (rows) for each column (variable)
        self.unassigned_columns = [i for i in range(n)]  # none of the columns are assigned yet
        self.backtrack_counter = 0
        
        if mrv:
            if inference == FC:
                self.solve_and_print(self.backtrack_improved, self.select_next_variable_improved, self.forward_checking)
            elif inference == AC3:
                self.solve_and_print(self.backtrack_improved, self.select_next_variable_improved, self.ac3)
            else:
                self.solve_and_print(self.backtrack, self.select_next_variable_improved)
        else:
            if inference == FC:
                self.solve_and_print(self.backtrack_improved, self.select_next_variable, self.forward_checking)
            elif inference == AC3:
                self.solve_and_print(self.backtrack_improved, self.select_next_variable, self.ac3)
            else:
                self.solve_and_print(self.backtrack, self.select_next_variable)


    def select_next_variable(self):
        """
        :return: Next unassigned variable (column) in line
        """

        return self.unassigned_columns[0]

    def is_consistent(self, col, val):
        """
        Check if assigning val to col will be consistent with the rest of the assigments
        :return: true of consistent, false otherwise
        """
        assigned_columns = [i for i in range(self.n) if i != col and i not in self.unassigned_columns]
        for i in assigned_columns:
            col_distance = abs(i - col)
            row_distance = abs(self.assignment[i] - val)
            if row_distance == 0 or row_distance == col_distance:
                return False
        return True

    def select_next_variable_improved(self):
        """
        Finds and returns the variable with the fewest legal values
        :return: Variable with the least amount of legal values
        """

        legal_moves = {}

        for var in self.unassigned_columns:
            legal_moves[var] = 0
            for val in self.domain[var]:
                if self.is_consistent(var, val):
                    legal_moves[var] += 1
        
        return min(legal_moves, key=legal_moves.get)

    def forward_checking(self, var):
        """
        Updates the domain of values and returns it
        :param var: Current column to check
        :return: Updated domain
        """

        new_domain = self.domain.copy()
        new_domain[var] = [self.assignment[var]]

        for col in self.unassigned_columns:
            for val in range(self.n):
                if val not in new_domain[col]:
                    continue

                if not self.is_consistent(col, val):
                    new_domain[col].remove(val)
            
            if not new_domain[col]:
                return []
        
        return new_domain

    def ac3(self, var):
        """
        Updates the domain of values and returns it
        :param var: Current column to check
        :return: Updated domain
        """
        new_domain = self.domain.copy()
        new_domain[var] = [self.assignment[var]]

        queue = []
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    queue.append((i, j))

        #print(f"Queue: {queue}")

        while queue:
            X = queue.pop(0)
            i = X[0]
            j = X[1]
            if self.revise(i, j, new_domain):
                if len(new_domain[i]) == 0:
                    return []
                for k in range(self.n):
                    if k != j and k != i:
                        #print(f"Adding ({k}, {i}) back to the queue")
                        queue.append((k, i))
        
        #print(f"New domain: {new_domain}")

        return new_domain
    
    def revise(self, i, j, new_domain):
        #print("I'm being revised")
        revised = False
        #print(f"New domain: {new_domain[i]}")
        #print(f"i: {i} and j: {j}")
        
        for x in range(self.n):
            if x not in new_domain[i]:
                continue

            if not self.is_consistent(i, x):
                new_domain[i].remove(x)
                revised = True
                continue

            consistent = False
            assigned = False

            if i in self.unassigned_columns:
                self.assignment[i] = x
                self.unassigned_columns.remove(i)
                assigned = True

            for y in range(self.n):
                if y not in new_domain[j]:
                    continue

                if self.is_consistent(j, y):
                    consistent = True

            if not consistent:
                #print(f"Removing {x} from domain of {i}")
                new_domain[i].remove(x)
                revised = True

            if assigned:
                self.assignment[i] = -1
                self.unassigned_columns.append(i)
                assigned = False

        return revised
            
    def backtrack(self, select_next_variable_method):
        """
           Recursive backtracking function that receives the current solution as an array
           :return:a solution (final problem state) if there is one, otherwise it returns [].
           """
        self.backtrack_counter += 1
        if len(self.unassigned_columns) == 0:
            return self.assignment

        # Select the next unassigned column
        var = select_next_variable_method()

        # Iterate through values for var
        for val in self.domain[var]:
            if self.is_consistent(var, val):
                self.assignment[var] = val
                self.unassigned_columns.remove(var)

                result = self.backtrack(select_next_variable_method)
                if result:
                    return result

                self.assignment[var] = -1
                self.unassigned_columns.append(var)  # reassign var to the unassigned columns

        return []

    def backtrack_improved(self, select_next_variable_method, inference=None):
        """
        Recursive backtracking function
        :param inference: an inference method such as forward chaining or ac3
        :return:a solution (final problem state) if there is one, otherwise it returns [].
        """

        self.backtrack_counter += 1

        self.backtrack_counter += 1
        if len(self.unassigned_columns) == 0:
            return self.assignment

        # Select the next unassigned column
        var = select_next_variable_method()

        # Iterate through values for var
        for val in range(self.n):
            if val not in self.domain[var]:
                #print(f"{val} is not in the domain of {var}")
                continue
            #print(f"Val: {val}")

            if self.is_consistent(var, val):
                #print(f"Assigning {var}={val}")
                #print(f"Domain: {self.domain}")
                self.assignment[var] = val
                self.unassigned_columns.remove(var)
                inferences = inference(var)

                if inferences:
                    #print(f"Made an inference")
                    #print(f"Inferences: {inferences}")
                    self.domain = inferences.copy()
                    result = self.backtrack_improved(select_next_variable_method, inference)
                
                    if result:
                        return result
                
                self.assignment[var] = -1
                self.unassigned_columns.append(var)  # reassign var to the unassigned columns
                self.reset_domain()
                #print("backed up")

        return []
    
    def reset_domain(self):
        for col in range(self.n):
            if col in self.unassigned_columns:
                self.domain[col] = list(range(self.n))
            else:
                self.domain[col] = [self.assignment[col]]

    def solve_and_print(self,  backtrack_method, select_next_variable_method, inference = None):

        if inference is None:
            self.solution = backtrack_method(select_next_variable_method)
        else:
            self.solution = backtrack_method(select_next_variable_method, inference)

        if self.solution.count(-1) == len(self.solution):
            print('Sorry, there is no solution to the %d-queens problem.' % (self.n))
        else:
            print('Solution: ' + str(self.solution))
            for x in range(0, self.n):
                for y in range(0, self.n):
                    if self.solution[x] == y:
                        print('Q', end=' ')
                    else:
                        print('-', end=' ')
                print('')

        print(self.backtrack_counter)


#nq = nQueens(4)
#nq = nQueens(5, False)
#nq = nQueens(30, False)
nq = nQueens(10)
# nq = nQueens(4, False,  FC)
# nq = nQueens(4, False,  AC3)
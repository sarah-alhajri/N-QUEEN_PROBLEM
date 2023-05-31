class NQueens:

    """The problem of placing N queens on an NxN board with none attacking
    each other. A state is represented as an N-element array, where
    a value of r in the c-th entry means there is a queen at column c,
    row r, and a value of -1 means that the c-th column has not been
    filled in yet. We fill in columns left to right."""

    def __init__(self, n):
        self.init_state = list([-1] * n)
        self.n = n

    def actions(self, state):
        """Return the actions that can be executed in the given
           state. The result is a list of valid actions"""

        if state[-1] != -1:  # all columns are filled
            return []  # no valid actions

        valid_actions = list(range(self.n))
        # In the leftmost empty column, try all non-conflicting rows
        col = state.index(-1)
        for row in range(self.n):
            for c, r in enumerate(state[:col]):

                if self.conflict(row, col, r, c) and row in valid_actions:
                    valid_actions.remove(row)
        return valid_actions

    def result(self, state, action):
        """Return the state that results from executing the given
          action in the given state. When expanding new children for each action in the valid actions
          list this function will be called to generate the new state"""
        col = state.index(-1)  # leftmost empty column
        new = list(state[:])
        new[col] = action  # queen's location
        return list(new)

    def goal_test(self, state):
        """Return True if the state is a goal. By checking if there is an empty column
        it will return false otherwise, checks if there is a conflict in case none true will
        be returned indicating this state is the goal state."""
        if state[-1] == -1:  # if there is an empty column
          return False  # then, state is not a goal state

        for c1, r1 in enumerate(state):
         for c2, r2 in enumerate(state):
             if (r1 != r2) and (c1 != c2) and self.conflict(r1, c1, r2, c2):
               return False
         return True

    def conflict(self, row1, col1, row2, col2):
        return row1 == row2 or col1 == col2 or abs(row1 - row2) == abs(col1 - col2)

    def g(self, cost):
        """Return the path cost, for each action the cost will be one."""
        return cost + 1

    def h(self, state):
        """Return number of conflicting queens for a given state"""
        conflicts = 0
        for col1, row1 in enumerate(state):
            for col2, row2 in enumerate(state[col1 + 1:], start=col1 + 1):
                if self.conflict(row1, col1, row2, col2):  # if conflict, add 2 to the current conflict value
                    conflicts += 2
        return conflicts


class Node:
    """Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node."""
    def __init__(self, state, parent=None, action=None,
                 path_cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.heuristic = heuristic
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def expand(self, problem):  # Returns a list of child nodes
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]




class NodeA(Node):  # A* Node
    def __init__(self, state, parent=None, action=None, path_cost=0, heuristic=0):
        super().__init__(state, parent, action, path_cost, heuristic)

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        next_node = NodeA(next_state, self, action,
                          problem.g(self.path_cost),
                          problem.h(next_state))
        return next_node

    def __lt__(self, other):
        return (self.path_cost + self.heuristic) < (other.path_cost + other.heuristic)


class NodeB(Node):  # BFS Node
    def __init__(self, state, parent=None, action=None, path_cost=0):
        super().__init__(state, parent, action, path_cost)

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        next_node = NodeB(next_state, self, action,
                          problem.g(self.path_cost))
        return next_node


class NodeI(Node):
    def __init__(self, state, parent=None, action=None, path_cost=0):
        super().__init__(state, parent, action, path_cost)

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        next_node = NodeI(next_state, self, action,
                          problem.g(self.path_cost))
        return next_node





import Board
import heapq



def searchA(node, problem):

    maxsize = 1
    frontier = [node]
    heapq.heapify(frontier)
    expanded = []
    while frontier:
        if maxsize < len(frontier):
            maxsize = len(frontier)
        current = heapq.heappop(frontier)

        print(current.state)
        if problem.goal_test(current.state):  # goal found
            print('The frontier maximum size: ' + str(maxsize))
            print('The total number of nodes generated before reaching a solution (search cost): ' + str(len(expanded)))
            return current

        children = current.expand(problem)  # expand child
        expanded.append(current)
        for i in children:
            if i not in expanded:
                heapq.heappush(frontier, i)
    return Board.Node(0, None, None)  # if frontier is empty, no solution


def searchB(node, problem):

    # check if goal found(check before add it to frontier) however this case will not happen,
    # since the initial state is not the goal.
    """if problem.goal_test(node.state):
        print('The frontier maximum size: ' + str(0))
        print('The total number of nodes generated before reaching a solution (search cost): ' + str(len(1)))
        print(node.state)
        return node"""
    frontier = [node]
    max_s_f = 0

    expanded = []
    while frontier:
        current = frontier.pop(0)  # FIFO
        print(current.state)

        children = current.expand(problem)  # expand child
        expanded.append(current)
        for i in children:
            if i not in expanded:
                if len(frontier) > max_s_f:
                    max_s_f = len(frontier)
                if problem.goal_test(i.state):  # goal found
                    print('The frontier maximum size: ' + str(max_s_f))
                    print('The total number of nodes generated before reaching a solution (search cost): ' + str(len(expanded)))
                    return i
                frontier.append(i)
    return Board.Node(0, None, None)  # if frontier is empty, no solution


def IDsearch(node, problem):
    i = 0
    node2, flag = DLsearch(node, problem, i)
    while flag == False:
        i = i+1
        node2, flag = DLsearch(node, problem, i)
    return node2

def DLsearch(node, problem, maxdepth):
    depth = 0
    frontier = [node]
    fmaxsize = 1
    expanded = []
    while frontier:
        if fmaxsize < len(frontier):
            fmaxsize = len(frontier)
        current = frontier.pop()
        print(current.state)
        if problem.goal_test(current.state):  # goal found
            print('The frontier maximum size: ' + str(fmaxsize))
            print('The total number of nodes generated before reaching a solution (search cost): ' + str(len(expanded)))
            return current, True


        children = current.expand(problem)  # expand child

        depth += 1

        expanded.append(current)
        for i in children:
            if i not in expanded:
                frontier.append(i)

        if depth>maxdepth:
            return current, False
    return Board.Node(0, None, None), True  # if frontier is empty or maximum depth is reached and no goal is found, no solution



def take_input():
    """Accepts the size of the chessboard"""

    while True:
        try:
            size = int(input('What is the size of the chessboard? n = \n'))
            if size == 1:
                print("Trivial solution, choose a board size of at least 8")
            if size <= 7 or size >= 15:
                print("Enter a value. Such that 7<size<15")
                continue
            return size
        except ValueError:

            print("Invalid value. Enter again")


print('Please enter the number strategy you want to test:')
while True:
    try:

        print('1. A*')
        print('2. BFS')
        print('3. IDS')
        print('Note: Write any number if you want to say: Goodbye.')
        num = int(input())
        if num == 1:
            print('You are in A* strategy!')
            size = take_input()
            board = Board.NQueens(size)
            nodeA = Board.NodeA(board.init_state, heuristic=board.h(board.init_state))
            a_star = searchA(nodeA, board)
            print('A-star solution: ' + str(a_star.state))
            print('The solution cost: ' + str(a_star.path_cost))
        elif num == 2:
            print('You are in BFS strategy!')
            size = take_input()
            board = Board.NQueens(size)
            nodeB = Board.NodeB(board.init_state)
            BFS = searchB(nodeB, board)
            print('BFS solution: ' + str(BFS.state))
            print('The solution cost: ' + str(BFS.path_cost))
        elif num == 3:
            print('You are in IDS strategy!')
            size = take_input()
            board = Board.NQueens(size)
            nodeI = Board.NodeI(board.init_state)
            IDS = IDsearch(nodeI, board)
            print('IDS solution: ' + str(IDS.state))
            print('The solution cost: ' + str(IDS.path_cost))

        else:
            print('Goodbye!')
            break
    except ValueError:
        print("Make sure to write the choice as numeric value (1, 2, or 3). Try again.")






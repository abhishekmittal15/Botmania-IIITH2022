from move_to_diagonal import solution
from pprint import pprint

row = [0] * 15
board = []
for i in range(15):
    board.append(row.copy())
board[0][0] = 1
board[0][1] = 1
board[0][2] = 1
board[0][3] = 1

board[1][0] = 1
board[1][1] = 1
board[1][2] = 1

board[2][0] = 1
board[2][1] = 1

board[3][0] = 1

state = {"hill": [0, 14], "board": board}
for i in range(400):
    print("Iteration ", i)
    move = solution(state)
    if (move == ()):
        continue
    print(move)
    
    state["hill"] = [(state["hill"][0] + 1) % 15, (state["hill"][1] - 1) % 15]
    
    board[move[1]][move[0]] = 0
    board[move[4]][move[3]] = 1
    state["board"] = board

    pprint(state["board"])
    print()

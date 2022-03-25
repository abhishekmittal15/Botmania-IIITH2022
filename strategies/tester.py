from move_to_diagonal import solution
import random
import json
from pprint import pprint

def main():
    random.seed(10)
    board = []
    choices = [0]
    for i in range(15):
        row = []
        for j in range(15):
            row.append(random.choice(choices))
        board.append(row)

    # with open('inp.json','w') as f:
    #     json.dump(board,f)

    with open('inp.json','r') as f:
        board = json.load(f)

    hill = (12,2)
    state={
        'hill' : hill,
        'board' : board
    }
    action_tuple = solution(state)
    pprint(board)
    print(f"Action : {action_tuple}")

if __name__=="__main__":
    main()

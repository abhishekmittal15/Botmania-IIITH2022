def dist(pt1,pt2):
    x1,y1=pt1
    x2,y2=pt2
    return abs(x1-x2)+abs(y1-y2)

def enemy_near(troop,board):
    return None

def solution(state : dict):
    # flip the hill co-ordinates 
    hill_position = state['hill'][1],state['hill'][0]
    board = state['board']
    army = []
    action_tuple=()

    # iterate over the board and get the positions of the troops 
    for idx,row in enumerate(board):
        for idy,col in enumerate(row):
            if col == 1 :
                army.append((idx,idy))

    # check if enemy is next to any one of the troops, if yes shoot it and return 
    for troop in army:
        enemy = enemy_near(troop,board)
        if enemy:
            return ("nuke",enemy[1],enemy[0])

    # if no, find the closest troop to the anti diagonal and check if the next cell is 0 and return the move 
    # closest_troop=-1
    # for troop in army:
    #     closest_distance=100
    #     for i in range(15):
    #         closest_distance=min(closest_distance,(i,14-i))


    return action_tuple

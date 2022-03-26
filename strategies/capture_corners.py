from collections import deque
from math import inf
from pprint import pprint
import random


def dist(pt1,pt2):
    x1,y1=pt1
    x2,y2=pt2
    return abs(x1-x2)+abs(y1-y2)

def enemy_near(troop,board):
    x,y = troop
    directions = [(0,-1),(1,0),(0,1),(-1,0)]
    for dx,dy in directions:
        nx,ny=x+dx,y+dy
        if(nx<0 or nx>14 or ny<0 or ny>14):
            continue
        if board[nx][ny] == 2:
            return (nx,ny)

    return None

def get_neighbour_list(x,y):
    neighbours=[]
    directions = [(0,-1),(1,0),(0,1),(-1,0)]
    random.shuffle(directions)
    for dx,dy in directions:
        nx,ny=x+dx,y+dy
        if nx<0 or nx>14 or ny<0 or ny>14:
            continue
        neighbours.append((nx,ny))
    return neighbours

def get_neighboring_diagonal(x,y):
    neighbours = []
    directions = [(1, -1), (-1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if nx < 0 or nx > 14 or ny < 0 or ny > 14:
            continue
        neighbours.append((nx, ny))
    return neighbours

def bfs(troop,board):
    q = deque([troop])
    visited = set()
    parent={}
    parent[troop]=troop
    distance=-1
    ans=[]
    visited.add(troop)
    while q and not ans:
        sz=len(q)
        distance+=1
        for _ in range(sz):
            x,y = q.popleft()
            if x+y==14:
                ans.append((x,y))
                continue
            # get the initial neighbours list 
            for nx,ny in get_neighbour_list(x,y):
                if board[nx][ny] in [1,2] or (nx,ny) in visited:
                    continue
            # validate each of the initial neighbours, if enemy in next neighbours
                nneighbours = get_neighbour_list(nx,ny)
                enemy = any(board[nnx][nny]==2 for nnx,nny in nneighbours)
                if enemy:
                    continue
                q.append((nx,ny))
                parent[(nx,ny)]=x,y
                visited.add((nx,ny))

    if ans==[]:
        return inf,-4,None,troop

    priority_diagonal_cells=[]
    # Now we have a list of all the diagonal elements which are 
    # 2. Empty/non-visible and no troop in above or below diagonal cell 
    # 1. Empty and no troop in below and above diagonal cell 
    for x, y in ans:
        # print(x, y)
        prio = 10 if (x,y) in [(13,1),(1,13)] else 0
        prio = -10 if (x,y) in [(14,0),(0,14)] else prio
        for nx, ny in get_neighboring_diagonal(x, y):
            val = board[nx][ny]
            if val == 0:
                prio += 2
            elif val == 1:
                prio += 0
            elif val == -1:
                prio += 1
            elif val == 2:
                prio -= 1
            else:
                assert False
            # print(nx, ny, board[nx][ny], prio)
        priority_diagonal_cells.append((-prio, (x, y)))
    # print(priority_diagonal_cells)
    priority_diagonal_cells.sort()
    prio,cell_chosen = priority_diagonal_cells[0]

    while parent[cell_chosen]!=troop:
        cell_chosen=parent[cell_chosen]

    return distance,prio,cell_chosen,troop

def solution(state : dict, enemy_diagonals = []):


    # flip the hill co-ordinates 
    hill_position = state['hill'][1],state['hill'][0]
    board = state['board']
    army = []
    action_tuple=()

    # iterate over the board and get the positions of the troops 
    # Iterate over the board and update it with previous enemy troop locations
    for idx,row in enumerate(board):
        for idy,col in enumerate(row):
            if col == 1:
                army.append((idx,idy))
            if col == 2 and idx+idy==14:
                if (idx,idy) in enemy_diagonals:
                    continue
                enemy_diagonals.append((idx,idy))
            if col == 0 and idx+idy==14:
                if (idx,idy) in enemy_diagonals:
                        enemy_diagonals.remove((idx,idy))

    for x,y in enemy_diagonals:
        board[x][y] = 2

    # print(f"Army : {army}")

    # check if enemy is next to any one of the troops, if yes shoot it and return 
    for troop in army:
        enemy = enemy_near(troop,board)
        if enemy:
            return ("nuke",enemy[1],enemy[0])

    # if no, find the closest troop to the anti diagonal and check if the next cell is 0 and return the move 
    closest_troop=-1
    closest_global=100
    distances = list(map(lambda troop: bfs(troop,board),army))
    distances.sort()
    # pprint(distances)
    distances = list(filter(lambda x: x[0]!=0 , distances))

    if len(distances) == 0:
        return ()

    # choose the troop that has highest priority and is also the closest
    dist,_,new_loc,old_loc = distances[0]
    if dist == inf:
        return ()

    y2,x2 = new_loc
    y1,x1 = old_loc

    return (x1,y1,"walk",x2,y2)

from collections import deque
from math import inf
from pprint import pprint

def dist(pt1,pt2):
    x1,y1=pt1
    x2,y2=pt2
    return abs(x1-x2)+abs(y1-y2)

def enemy_near(troop,board):
    x,y = troop
    directions = [(-1,0),(1,0),(0,1),(0,-1)]

    for dx,dy in directions:
        nx,ny=x+dx,y+dy
        if(nx<0 or nx>14 or ny<0 or ny>14):
            continue
        if board[nx][ny] == 2:
            return (nx,ny)

    return None

def bfs(troop,board):
    q = deque([troop])
    visited = set()
    parent={}
    parent[troop]=troop
    distance=-1
    ans=None;
    directions = [(-1,0),(1,0),(0,1),(0,-1)]
    visited.add(troop)
    while q and not ans:
        sz=len(q)
        distance+=1
        for _ in range(sz):
            x,y = q.popleft()
            if x+y==14:
                ans=x,y
                break
            for dx,dy in directions:
                nx,ny=x+dx,y+dy
                if nx<0 or nx>14 or ny<0 or ny>14:
                    continue
                if board[nx][ny] in [1,2] or (nx,ny) in visited:
                    continue
                # print(nx,ny)
                q.append((nx,ny))
                parent[(nx,ny)]=x,y
                visited.add((nx,ny))
    if ans==None:
        return inf,None,troop

    while parent[ans]!=troop:
        ans=parent[ans]

    return distance,ans,troop

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

    dist,new_loc,old_loc = distances[0]
    if dist == inf:
        return ()

    y2,x2 = new_loc
    y1,x1 = old_loc

    return (x1,y1,"walk",x2,y2)

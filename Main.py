import API
import sys
from collections import deque


#Miar Taweel 1210447
#Francis Miadi 1210100
#Leena Abuhammd 1210460


print("start")

MAZE_SIZE = 16
wall = [[0 for _ in range(MAZE_SIZE)] for _ in range(MAZE_SIZE)]
queue = []
x = 0
y = 0
point = 0



def turnSide(num, turning):
    direction_map = {'L': -1, 'R': 1, 'B': 2}  # Mapping for turning
    if turning in direction_map:
        num = (num + direction_map[turning]) % 4
    return num


def newCoor(x, y, num):
    moves = {
        0: (0, 1),  # Move up
        1: (1, 0),  # Move right
        2: (0, -1), # Move down
        3: (-1, 0)  # Move left
    }
    dx, dy = moves.get(num, (0, 0))  # Default to no movement if num is invalid
    return x + dx, y + dy


def walls(x, y, orient, L, R, F):
    # Define mappings for each condition
    conditions = {
        (True, True, True): {0: 13, 1: 12, 2: 11, 3: 14},
        (True, True, False): {0: 9, 1: 10, 2: 9, 3: 10},
        (True, False, True): {0: 8, 1: 7, 2: 6, 3: 5},
        (False, True, True): {0: 7, 1: 6, 2: 5, 3: 8},
        (False, False, True): {0: 2, 1: 3, 2: 4, 3: 1},
        (True, False, False): {0: 1, 1: 2, 2: 3, 3: 4},
        (False, True, False): {0: 3, 1: 4, 2: 1, 3: 2},
    }

    # Check for specific conditions
    key = (L, R, F)
    if key in conditions:
        wall[y][x] = conditions[key][orient]
    else:
        # Default case if no walls
        wall[y][x] = 15

def reachable(x, y, x1, y1): # Determines if a block is reachable from the current spot

    # Define sets of blocking values for each direction
    block_up = {4, 5, 6, 10, 11, 12, 14}
    block_down = {2, 7, 8, 10, 12, 13, 14}
    block_left = {1, 5, 8, 9, 11, 13, 14}
    block_right = {3, 6, 7, 9, 11, 12, 13}

    # Check vertical movement
    if x == x1:
        if y > y1:  # Moving up
            if wall[y][x] in block_up or wall[y1][x1] in block_down:
                return False
        elif y < y1:  # Moving down
            if wall[y][x] in block_down or wall[y1][x1] in block_up:
                return False

    # Check horizontal movement
    elif y == y1:
        if x > x1:  # Moving left
            if wall[y][x] in block_left or wall[y][x1] in block_right:
                return False
        elif x < x1:  # Moving right
            if wall[y][x] in block_right or wall[y][x1] in block_left:
                return False

    # If none of the conditions block the movement, return True
    return True

def adjacents(x, y):
    # Define the four directions explicitly
    x0, y0 = x, y + 1  # North
    x1, y1 = x + 1, y  # East
    x2, y2 = x, y - 1  # South
    x3, y3 = x - 1, y  # West

    # Handle boundary conditions for east and north directions
    if x1 >= MAZE_SIZE:
        x1 = -1
    if y0 >= MAZE_SIZE:
        y0 = -1
    # Return the results in the correct order
    return (x0, y0, x1, y1, x2, y2, x3, y3)


flood=[[500 for _ in range(MAZE_SIZE)] for _ in range(MAZE_SIZE)]
distances = [[0 for _ in range(MAZE_SIZE)] for _ in range(MAZE_SIZE)]

#Starts from a goil point and calulates the distance without walls
def BFS_withoutwalls(maze, goalx, goaly):
    rows, cols = len(maze), len(maze[0])  # Get maze dimensions
    # Initialize all cells to 500 (unvisited)
    for y in range(rows):
        for x in range(cols):
            maze[y][x] = 500

    # Create a queue and set the destination point to distance 0
    queue = deque([(goalx, goaly)])
    maze[goaly][goalx] = 0

    # Perform BFS
    while queue:
        xrun, yrun = queue.popleft()  # Dequeue the current cell

        # Get adjacent cells using the `adjacents` function
        x0, y0, x1, y1, x2, y2, x3, y3 = adjacents(xrun, yrun)

        # Check and update each adjacent cell
        for nx, ny in [(x0, y0), (x1, y1), (x2, y2), (x3, y3)]:
            if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == 500:
                maze[ny][nx] = maze[yrun][xrun] + 1  # Update distance
                queue.append((nx, ny))  # Enqueue the cell


#Starts from the middle 2*2 and calulates the distance of each block from the goal
def floodFill(maze):
    rows, cols = len(maze), len(maze[0])  # Get maze dimensions
    # Initialize all cells to 500 (unvisited)
    for y in range(rows):
        for x in range(cols):
            maze[y][x] = 0
    maze[7][7] = 1
    maze[8][7] = 1
    maze[7][8] = 1
    maze[8][8] = 1
    # Initialize queue with the goal points
    queue = deque([(7, 7), (8, 7), (7, 8), (8, 8)])

    # Perform BFS
    while queue:
        xrun, yrun = queue.popleft()  # Dequeue the current cell
        x0, y0, x1, y1, x2, y2, x3, y3 = adjacents(xrun, yrun)
        for nx, ny in [(x0, y0), (x1, y1), (x2, y2), (x3, y3)]:
            if 0 <= nx < rows and 0 <= ny < rows and wall[ny][nx] != 0:
                if maze[ny][nx] == 0 and reachable(xrun, yrun, nx, ny):
                    maze[ny][nx] = maze[yrun][xrun] + 1  # Update distance
                    queue.append((nx, ny))


#Starts from the goal point and calulates the distance with walls
def BFS_withwalls(maze, queue):
    while queue:
        yrun = queue.pop(0)
        xrun = queue.pop(0)

        # Get adjacent cells using the `adjacents` function
        x0, y0, x1, y1, x2, y2, x3, y3 = adjacents(xrun, yrun)
        neighbors = [(x0, y0), (x1, y1), (x2, y2), (x3, y3)]

        # Process each neighbor
        for nx, ny in neighbors:
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze):  # Check bounds
                if maze[ny][nx] == 500:  # Check if the cell is unvisited
                    if reachable(xrun, yrun, nx, ny):  # Check reachability
                        maze[ny][nx] = maze[yrun][xrun] + 1  # Update distance
                        queue.append(ny)  # Enqueue the cell
                        queue.append(nx)

def nextBestDirection(maze, x, y, xprev, yprev, facing):

    # Get adjacent cells and initialize variables
    neighbors = adjacents(x, y)  # Returns (x0, y0, x1, y1, x2, y2, x3, y3)
    minVals = [1000] * 4  # Initial high values for each direction
    prev = -1
    # Loop through the 4 neighbors (north, east, south, west)
    for i in range(4):
        nx, ny = neighbors[i * 2], neighbors[i * 2 + 1]  # Extract neighbor coordinates
        if reachable(x, y, nx, ny):  # Check if reachable
            if nx == xprev and ny == yprev:  # Check if it's the previous cell
                prev = i
            minVals[i] = maze[ny][nx]

    # Determine the direction with the smallest value
    minCell = -1
    minVal = min(minVals)
    for i, val in enumerate(minVals):
        if val == minVal:
            if len([v for v in minVals if v != 1000]) == 1 or i != prev:
                minCell = i
                break

    # Determine the move direction based on the current orientation
    if minCell == facing:
        return 'F'
    elif minCell == (facing - 1) % 4:
        return 'L'
    elif minCell == (facing + 1) % 4:
        return 'R'
    else:
        return 'B'

def next_1destination(maze, x, y, xprev, yprev, orient):

    # Get adjacent cells
    neighbors = adjacents(x, y)  # (x0, y0, x1, y1, x2, y2, x3, y3)
    val = maze[y][x]
    minCell = None

    # Iterate through the 4 neighbors
    for i in range(4):
        nx, ny = neighbors[i * 2], neighbors[i * 2 + 1]  # Neighbor coordinates
        if reachable(x, y, nx, ny) and maze[ny][nx] == val - 1:
            minCell = i  # Assign the direction to minCell
            break

    # Determine the move direction based on the orientation
    if minCell == orient:
        return 'F'
    elif minCell == (orient - 1) % 4:
        return 'L'
    elif minCell == (orient + 1) % 4:
        return 'R'
    else:
        return 'B'

def OnMazePrint():
    for x in range(MAZE_SIZE):
        for y in range(MAZE_SIZE):

            API.setText(x, y, str(distances[y][x]))

def middlePart(x, y, facing):
    def update_and_move(x, y, facing, turn_direction=None):
        L = API.wallLeft()
        R = API.wallRight()
        F = API.wallFront()
        walls(x, y, facing, L, R, F)

        API.moveForward()
        x, y = newCoor(x, y, facing)

        if turn_direction:
            if turn_direction == 'R':
                API.turnRight()
            elif turn_direction == 'L':
                API.turnLeft()
            facing = turnSide(facing, turn_direction)

        return x, y, facing

    # Check the left wall and start the logic
    L = API.wallLeft()
    if L:
        for _ in range(4):  # Perform 4 moves with right turns
            x, y, facing = update_and_move(x, y, facing, 'R')
        xprev, yprev = x, y
        x, y, facing = update_and_move(x, y, facing)
    else:
        for _ in range(4):  # Perform 4 moves with left turns
            x, y, facing = update_and_move(x, y, facing, 'L')
        xprev, yprev = x, y
        x, y, facing = update_and_move(x, y, facing)

    return x, y, xprev, yprev, facing

def initializeFlood(value=500, center_coordinates=None):

    for i in range(MAZE_SIZE):
        for j in range(MAZE_SIZE):
            flood[i][j] = value

    if center_coordinates:
        for x, y in center_coordinates:
            flood[y][x] = 0


def addCenterToQ():

    # Initialize the grid and center to `0`
    initializeFlood(center_coordinates=[(7, 7), (8, 7), (7, 8), (8, 8)])

    # Add center coordinates to the queue
    for x, y in [(7, 7), (8, 7), (7, 8), (8, 8)]:
        queue.append(y)
        queue.append(x)

def addGoalToQ(x, y):
    # Initialize the grid and set the destination to `0`
    initializeFlood(center_coordinates=[(x, y)])
    # Add destination coordinates to the queue
    queue.append(y)
    queue.append(x)

def perform_turn_and_move(direction, orient):
    if direction == 'L':
        API.turnLeft()
        orient = turnSide(orient, 'L')
    elif direction == 'R':
        API.turnRight()
        orient = turnSide(orient, 'R')
    elif direction == 'B':
        API.turnLeft()
        orient = turnSide(orient, 'L')
        API.turnLeft()
        orient = turnSide(orient, 'L')
    return orient

def log(string):
    sys.stderr.write("{}\n".format(string))


def main():

    xcurrent, ycurrent, xprev, yprev, facing = 0, 0, 0, 0, 0
    step = 0
    flag = False

    try:
        while True:
            # Get wall data and update walls
            L, R, F = API.wallLeft(), API.wallRight(), API.wallFront()
            walls(xcurrent, ycurrent, facing, L, R, F)

            # State logic
            if flood[ycurrent][xcurrent] != 0:

                if step == 0:
                    log("Finding the goal.....")
                    addCenterToQ()
                elif step == 1:
                    log("Discovering alternate flag paths .....")
                    addGoalToQ(15, 0)
                    flag = False
                elif step == 2:
                    log("Going back to start to find another path.....")
                    addGoalToQ(0, 0)
                    flag = False
                elif step == 3:
                    log("Finding another path if exists.....")
                    addCenterToQ()
                    floodFill(distances)
                    flag = False
                elif step == 4:
                    log("Shortest Path found, going back to start.....")
                    addGoalToQ(0, 15)
                    flag = False
                elif step == 5:
                    addGoalToQ(0, 0)
                    flag = False
                elif step == 6:
                    log("Taking the shortest path.....")
                    API.setColor(xcurrent, ycurrent, 'blue')
                    addCenterToQ()
                    floodFill(distances)
                    flag = True

                BFS_withwalls(flood, queue)

            else:
                if step == 5:
                    addCenterToQ()
                    BFS_withwalls(flood, queue)
                elif step == 4:
                    BFS_withoutwalls(flood, 0, 0)
                elif step == 3:
                    BFS_withoutwalls(flood, 0, 15)
                elif step == 2:
                    addCenterToQ()
                    BFS_withwalls(flood, queue)
                elif step == 1:
                    BFS_withoutwalls(flood, 0, 0)
                elif step == 0:
                    xcurrent, ycurrent, xprev, yprev, facing = middlePart(xcurrent, ycurrent, facing)
                    BFS_withoutwalls(flood, 15, 0)
                step += 1
                floodFill(distances)

            # Determine direction
            if flag:
                direction = next_1destination(distances, xcurrent, ycurrent, xprev, yprev, facing)
                if (xcurrent, ycurrent) in [(7, 7), (8, 7), (8, 8), (7, 8)]:
                    #Destination reached
                    break
            else:
                direction = nextBestDirection(flood, xcurrent, ycurrent, xprev, yprev, facing)

            # Perform turn and move
            facing = perform_turn_and_move(direction, facing)
            # Print maze and move forward
            OnMazePrint()
            API.moveForward()
            xprev, yprev = xcurrent, ycurrent
            xcurrent, ycurrent = newCoor(xcurrent, ycurrent, facing)

        log("GOAL REACHED")

    except API.MouseCrashedError:
        log("CRASH")


if __name__ == "__main__":
    main()
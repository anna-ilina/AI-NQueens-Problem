'''
Cisc 352 Assignment 3

Justin Gerolami - 10160479 - 14JG28
Anna Ilina - -
'''

import itertools
import heapq

#****************************************************************************#
#                               Class Cell                                   #
#****************************************************************************#
class Cell(object):
    def __init__(self, x, y, reachable):
        self.x = x
        self.y = y
        self.reachable = reachable

        #Store the parent so we can backtrack
        self.parent = None

        #Store the values for G, H, F,
        #F(node) = G(node) + H(node)
        self.g = 0
        self.h = 0
        self.f = 0



#****************************************************************************#
#                              Class AStar                                   #
#****************************************************************************#
class AStar(object):
    def __init__(self):
        self.goto = []
        heapq.heapify(self.goto)
        self.visited = set()
        self.cells = []
        self.numRows = None
        self.numCols = None

    def initMaze(self, rows, cols, walls, start, end):
        self.numRows = rows
        self.numCols = cols

        for i in range(self.numRows):
            for j in range(self.numCols):
                if (i,j) in walls:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(i,j,reachable))

        self.start = self.getCellAtLocation(start[0], start[1])
        self.end = self.getCellAtLocation(end[0], end[1])

    def getCellAtLocation(self, row, col):
        #returns the cell in the cell list.
        #The location of each row will be the row it is in * the total number of rows
        #We add the column value to get the specific cell
        return self.cells[row*self.numRows + col]

    def manhattanDistanceHeuristic(self, cell):
        #Manhattan distance is the distance from the current cell to the goal cell
        return abs(cell.x - self.end.x) + abs(cell.y - self.end.y)

    def findNeighbours(self,cell):
        neighbours = []
        #Get the one to the right
        if cell.x < self.numCols - 1:
            neighbours.append(self.getCellAtLocation(cell.x+1, cell.y))
        #Get the one above
        if cell.y > 0:
            neighbours.append(self.getCellAtLocation(cell.x, cell.y-1))
        #Get the one to the left
        if cell.x > 0:
            neighbours.append(self.getCellAtLocation(cell.x-1,cell.y))
        #Get the one below
        if cell.y < self.numRows-1:
            neighbours.append(self.getCellAtLocation(cell.x, cell.y+1))
        return neighbours

    def calculateF(self, neighbour, cell):
        #Fn = Gn + Hn
        #cost of path so far
        neighbour.g = cell.g + 1
        neighbour.h = self.manhattanDistanceHeuristic(neighbour)
        neighbour.f = neighbour.h + neighbour.g

        #Set the parent to the current cell
        neighbour.parent = cell

    def getPath(self):
        #Start at the end and work back through the parents
        cell = self.end
        #initial path is the end
        path = [(cell.x,cell.y)]

        #loop through until we reach the start
        while cell.parent is not self.start:
            cell = cell.parent
            #append the coordinates
            path.append((cell.x,cell.y))
        #append the start
        path.append((self.start.x, self.start.y))
        #reverse to it goes from start -> goal
        path.reverse()
        return path

    def findBestPath(self):
        #start with the start node - add to the goto heap the f value of start and the location
        heapq.heappush(self.goto, (self.start.f, self.start))

        #Loop until we have no more nodes left to visit
        while len(self.goto) != 0:
            #Pop the first thing in the heapq
            fVal, cell = heapq.heappop(self.goto)

            #add it to the visited list
            self.visited.add(cell)

            #Check if it is the goal
            if cell == self.end:
                return self.getPath()

            #It was not a goal
            else:
                #Get the neighbours
                neighbours = self.findNeighbours(cell)

                #Loop through the neighbours list
                for neighbour in neighbours:
                    #If we can get to it and it hasn't already been visited
                    if neighbour not in self.visited and neighbour.reachable == True:
                        #Check if it is currently in the heapq
                        if (neighbour.f, neighbour) in self.goto:
                            #Check if the new path is better
                            if neighbour.g > cell.g + 1:
                                #update it
                                self.calculateF(neighbour, cell)
                        else:
                            #If it was not better, calculate the F(node) and push it to our heapq
                            self.calculateF(neighbour, cell)
                            heapq.heappush(self.goto, (neighbour.f, neighbour))



#****************************************************************************#
#                           General Functions                                #
#****************************************************************************#
'''
Function: readMazeFromFile
Arguments: Takes a filename as its argument and will read the data.
Returns: a list of maze data

This filename will be pathfinding.txt, a file containing N mazes in the form:

XXXXXXXXXX
X___XX_X_X
X_X__X___X
XSXX___X_X
X_X__X___X
X___XX_X_X
X_X__X_X_X
X__G_X___X
XXXXXXXXXX

These mazes are all read into a list, and returned.
'''
def readMazeFromFile(filename='pathfinding.txt'):
    mazes = [];
    with open(filename, 'r') as f:
        mazes = f.read().splitlines()
    f.close()
    return mazes

'''
Function: splitIntoSeparateMazes
Arguments: - Iterable: A list which contains elements, in this case it is a list of mazes.
           - splitters: The characters that the list will be split on. We set the default
                        to be a space because the text file containing the mazes has a space between mazes.
Returns: A list of lists which were split on 'splitters' (space), where each sublist represents the individual maze.
'''
def splitIntoSeparateMazes(iterable, splitters=""):
        return [list(g) for k, g in itertools.groupby(iterable, lambda x: x in splitters) if not k]

'''
Function: findStart
Arguments: A maze list
Returns: The x and y starting position in the maze
'''
def findStart(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 'S' or maze[i][j] == 's':
                return [i,j]

    print("Error: Did not find a starting position")
    return None


'''
Function: findEnd
Arguments: A maze list
Returns: The x and y goal position in the maze
'''
def findEnd(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 'G' or maze[i][j] == 'g':
                return [i,j]

    print("Error: Did not find a goal position")
    return None


'''
Function: findWalls
Arguments: A maze list
Returns: The x and y positions of all the walls in the maze
'''
def findWalls(maze):
    walls = []
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 'X' or maze[i][j] == 'x':
                walls.append([i,j])
    return walls


def main():
    mazes = readMazeFromFile()
    mazes = splitIntoSeparateMazes(mazes)
    #print("List of lists of mazes: " + str(mazes))

    #Loop through all the mazes
    for maze in mazes:
        #Create Astar object
        Grid = AStar()

        #Get the details of the maze
        numRows = len(maze)
        numCols = len(maze[0])
        startPos = findStart(maze)
        endPos = findEnd(maze)
        walls = findWalls(maze)

        #initialize the maze
        Grid.initMaze(numRows, numCols,walls, startPos, endPos)

        #solve the maze
        pathList = Grid.findBestPath()
        print(pathList)
        finalPath = []
        for i in range(numRows):
            path = []
            for j in range(numCols):
                if (i,j) in pathList:
                    path.append('P')
                else:
                    path.append(maze[i][j])
            finalPath.append(path)

        #print the path
        for i in range(numRows):
            print(finalPath[i])
        print("")


if __name__ == '__main__':
    main()

'''
Cisc 352 Assignment 3

Justin Gerolami - 10160479 - 14JG28
Anna Ilina - -
'''

import itertools
import heapq
import os

#****************************************************************************#
#                               Class Cell                                   #
#****************************************************************************#
'''
Class Cell will hold information on each individual cell in the maze
Input Parameters: X location, Y location, Boolean reachable if it is a wall or not
'''
class Cell(object):
    '''Constructor initializes'''
    def __init__(self, x, y, reachable):
        #Set the location and if it is a wall or not
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
#                            Class AStar4Directions                          #
#****************************************************************************#
'''
Class AStar4Directions is the class that solves the maze using the A* search,
and will only go up, right, down, left.
'''
class AStar4Directions(object):
    ''' Constructor to set the size, holds cells, holds heapq'''
    def __init__(self):
        #Holds the cells we will go to next
        self.goto = []
        #Turn goto into a heap queue
        heapq.heapify(self.goto)
        #Create a set to keep track of what cells we have gone to
        self.visited = set()
        #Hold a list of cells
        self.cells = []
        #Set the size of the maze
        self.numRows = None
        self.numCols = None


    '''
    Function: initMaze
    Parameters: maze
    initMaze() will initialize the settings of the maze. It will set the size, get the start and goal positions,
    find the walls, set each cell to reachable or not, and then add it to the cells list
    '''
    def initMaze(self, maze):
        #Set up the maze
        self.maze = maze
        self.numRows = len(maze)
        self.numCols = len(maze[0])

        #get the start, end, walls
        self.startPos = self.findStart()
        self.endPos = self.findEnd()
        walls = self.findWalls()

        #Loop through, determine if wall or not and set reachable
        for i in range(self.numCols):
            for j in range(self.numRows):
                if [i,j] in walls:
                    reachable = False
                else:
                    reachable = True
                #add the cell to the cells list
                self.cells.append(Cell(i,j,reachable))

        #Convert the start and end positions to the location in the cells list
        self.start = self.getCellAtLocation(self.startPos[0], self.startPos[1])
        self.end = self.getCellAtLocation(self.endPos[0], self.endPos[1])


    '''
    Function: findStart
    Returns: The x and y starting position in the maze
    '''
    def findStart(self):
        #loop through rows and cols
        for i in range(self.numRows):
            for j in range(self.numCols):
                #Check for start position, if true, return it
                if self.maze[i][j] == 'S' or self.maze[i][j] == 's':
                    return [i, j]

        #If we get here there is no start position
        print("Error: Did not find a starting position")
        return None


    '''
    Function: findEnd
    Returns: The x and y goal position in the maze
    '''
    def findEnd(self):
        #loop through rows and cols
        for i in range(self.numRows):
            for j in range(self.numCols):
                #check for goal position, if true return
                if self.maze[i][j] == 'G' or self.maze[i][j] == 'g':
                    return [i, j]
        #If we get here there is no goal position
        print("Error: Did not find a goal position")
        return None


    '''
    Function: findWalls
    Returns: The x and y positions of all the walls in the maze
    '''
    def findWalls(self):
        #hold the list of walls
        walls = []
        #Loop through rows and cols
        for i in range(self.numRows):
            for j in range(self.numCols):
                #if it is a wall, add it to the wall list
                if self.maze[i][j] == 'X' or self.maze[i][j] == 'x':
                    walls.append([i, j])
        #return the wall positons
        return walls


    '''
    Function: getCellAtLocation
    Parameters: Row and col of what cell we want
    Returns: The cell in the cell list
    '''
    def getCellAtLocation(self, row, col):
        #returns the cell in the cell list.
        #The location of each row will be the row it is in * the total number of rows
        #We add the column value to get the specific cell
        return self.cells[row*self.numRows + col]


    '''
    Function DistanceHeuristic
    Parameters: Cell of current position
    Returns: The manhattan distance (exact value in this case) to the goal from the cell
    '''
    def DistanceHeuristic(self, cell):
        #Manhattan distance is the distance from the current cell to the goal cell
        return abs(cell.x - self.end.x) + abs(cell.y - self.end.y)


    '''
    Function: findNeighbours
    Parameters: Cell to find neighbours of
    Returns: List of all neighbours of the cell
    '''
    def findNeighbours(self,cell):
        #holds the neighbours of the cell
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


    '''
    Function: calculateF
    Parameters: neighbour cell and current cell
    Updates the Fn, Gn, Hn values of the neighbour, sets the current cell as the parent
    '''
    def calculateF(self, neighbour, cell):
        #Fn = Gn + Hn
        #Add one to Gn because we moved 1 cell in some direction
        neighbour.g = cell.g + 1
        #Get the manhattan distance for the new cell
        neighbour.h = self.DistanceHeuristic(neighbour)
        #Calculate its Fn
        neighbour.f = neighbour.h + neighbour.g
        #Set the parent to the current cell
        neighbour.parent = cell


    '''
    Function: getPath
    Returns: The coordinates of the path that the maze took
    getPath() starts at the goal node and works its way back by looking at the parent cell of the current cell.
    The parent is added to a path list, and once finished, the list is reversed to make the path go from start->goal
    '''
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


    '''
    Function: findBestPath
    Returns: The best path as found by the A* algorithm. Returns none if there is no possible path
    findBestPath() uses a heapq to push cells onto. This will keep track of the one we should go to next based on
    the Fn value. We loop while we have things to go to and pop from the queue. We add the cell to the visited, and check
    if it is a goal. If it is a goal, we can return, otherwise we get the neighbours and push it onto the queue.
    '''
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
            if cell is self.end:
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
        #we did not find a path
        return None


#****************************************************************************#
#                            Class Greedy4Directions                         #
#****************************************************************************#
'''
Class Greedy4Directions extends AStar4Directions because it uses the exact same method as A*
The only difference in Greedy is it does not use Gn in the calculation and just looks at the
heuristic value. This class has 1 override function, calculateF() which simply sets Gn to 0
'''
class Greedy4Directions(AStar4Directions):
    '''Override functions from AStar4Directions'''

    '''
    Function: calculateF
    Parameters: neighbour cell and current cell
    Updates the Fn, Gn, Hn values of the neighbour, sets the current cell as the parent
    '''
    def calculateF(self, neighbour, cell):
        # Fn = Gn + Hn
        # Set Gn to 0 because we are using greedy.
        # We need to keep Gn here because functions in AStar4Directions use it
        neighbour.g = 0
        # Get the manhattan distance for the new cell
        neighbour.h = self.DistanceHeuristic(neighbour)
        # Calculate its Fn
        neighbour.f = neighbour.h + neighbour.g
        # Set the parent to the current cell
        neighbour.parent = cell


# ****************************************************************************#
#                          Class AStar5Directions                             #
# ****************************************************************************#
'''
Class AStar5Directions extends AStar4Directions
It overrides the DistanceHeuristic function from manhattan to chebyshev, and also
overrides the findNeighbours function to allow for diagonals
'''
class AStar5Directions(AStar4Directions):
    '''Override Functions'''
    '''
        Function DistanceHeuristic
        Parameters: Cell of current position
        Returns: The Chebyshev distance (exact value in this case) to the goal from the cell
        '''
    def DistanceHeuristic(self, cell):
        # Chebyshev distance looks at all possible neighbours and takes max so we overestimate
        return max(abs(cell.x - self.end.x),abs(cell.y - self.end.y))


    '''
    Function: findNeighbours
    Parameters: Cell to find neighbours of
    Returns: List of all neighbours of the cell
    '''
    def findNeighbours(self, cell):
        # holds the neighbours of the cell
        neighbours = []
        # Get the one to the right
        if cell.x < self.numCols - 1:
            neighbours.append(self.getCellAtLocation(cell.x + 1, cell.y))
        # Get the one above
        if cell.y > 0:
            neighbours.append(self.getCellAtLocation(cell.x, cell.y - 1))
        # Get the one to the left
        if cell.x > 0:
            neighbours.append(self.getCellAtLocation(cell.x - 1, cell.y))
        # Get the one below
        if cell.y < self.numRows - 1:
            neighbours.append(self.getCellAtLocation(cell.x, cell.y + 1))
        #Below, right
        if cell.x < self.numCols -1 and cell.y < self.numRows -1:
            neighbours.append(self.getCellAtLocation(cell.x+1, cell.y+1))
        #Above Right
        if cell.x < self.numCols - 1 and cell.y > 0:
            neighbours.append(self.getCellAtLocation(cell.x + 1, cell.y - 1))
        #Above Left
        if cell.x > 0 and cell.y > 0:
            neighbours.append(self.getCellAtLocation(cell.x-1, cell.y-1))
        #Below Left
        if cell.x > 0 and cell.y < self.numRows-1:
            neighbours.append(self.getCellAtLocation(cell.x-1, cell.y+1))
        return neighbours


# ****************************************************************************#
#                          Class Greedy5Directions                            #
# ****************************************************************************#
'''
Class Greedy5Directions extends AStar5Directions, which extends AStar4Directions
Greedy5Directions overrides the calculateF function, setting Gn to 0 because this
is not used in greedy searches
'''
class Greedy5Directions(AStar5Directions):
    '''Override functions from AStar5Directions'''
    '''
    Function: calculateF
    Parameters: neighbour cell and current cell
    Updates the Fn, Gn, Hn values of the neighbour, sets the current cell as the parent
    '''
    def calculateF(self, neighbour, cell):
        # Fn = Gn + Hn
        # Set Gn to 0 because we are using greedy.
        # We need to keep Gn here because functions in AStar4Directions use it
        neighbour.g = 0
        # Get the manhattan distance for the new cell
        neighbour.h = self.DistanceHeuristic(neighbour)
        # Calculate its Fn
        neighbour.f = neighbour.h + neighbour.g
        # Set the parent to the current cell
        neighbour.parent = cell


#****************************************************************************#
#                           General Functions                                #
#****************************************************************************#
'''
Function: readMazeFromFile
Parameters: Takes a filename as its parameter and will read the data.
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
def readMazeFromFile(filename):
    #holds the input
    mazes = [];
    #While the file is open
    with open(filename, 'r') as f:
        #read the lines
        mazes = f.read().splitlines()
    #close the file
    f.close()

    #Check if there is already pathfinding_out.txt and if so, remove it.
    #This allows us to append each maze to the output with ease.
    if filename == "pathfinding_a.txt":
        if os.path.isfile("pathfinding_a_out.txt"):
            os.remove("pathfinding_a_out.txt")
    elif filename == "pathfinding_b.txt":
        if os.path.isfile("pathfinding_b_out.txt"):
            os.remove("pathfinding_b_out.txt")
    #return the input read
    return mazes


'''
Function: writeMazeToFile
Parameters: number of rows, the final solved maze, alg used, and a filename default to pathfinding_out.txt
writeMazeToFile() will write each solved maze to the output file.
The format is: A* maze, Greedy maze, blank line, repeat until done
'''
def writeMazeToFile(numRows, finalPath, alg, filename):
    #open the file for appending
    with open(filename, 'a') as f:
        #write the alg used
        f.write(alg + "\n")
        #prints the maze into the file in proper format
        for i in range(numRows):
            f.writelines(finalPath[i])
            f.write("\n")
        #Blank line to separate after Greedy
        if alg == "GREEDY":
            f.write("\n")
    #close file
    print("Ouput saved in "+ filename)
    f.close()


'''
Function: splitIntoSeparateMazes
Parameters: - Iterable: A list which contains elements, in this case it is a list of mazes.
           - splitters: The characters that the list will be split on. We set the default
                        to be a space because the text file containing the mazes has a space between mazes.
Returns: A list of lists which were split on 'splitters' (space), where each sublist represents the individual maze.
'''
def splitIntoSeparateMazes(iterable, splitters=""):
        #Fast way to convert into list of lists
        return [list(g) for k, g in itertools.groupby(iterable, lambda x: x in splitters) if not k]


'''
Function: getFinalPathAsList
Parameters: Grid object and path list of coordinates
Returns: Modified maze in proper format with the path replaced from '_' to 'P'
'''
def getFinalPathAsList(Grid, pathList):
    #holds the path
    finalPath = []
    #loop through the rows
    for i in range(Grid.numRows):
        #another list to hold each row
        path = []
        #loop through the columns
        for j in range(Grid.numCols):
            #Check if the location is the start position, append S
            if [i, j] == Grid.startPos:
                path.append('S')
            #Check if the location is the end position, append G
            elif [i, j] == Grid.endPos:
                path.append('G')
            #Check if the location is part of the path, append P
            elif (i, j) in pathList:
                path.append('P')
            #Append whatever was in the location in the original maze
            else:
                path.append(Grid.maze[i][j])
        #Append each row to the finalPath list
        finalPath.append(path)
    #return the final path
    return finalPath


'''
Function: partA4Directions:
partA4Directions() is used for running part A of the assignment using up down left and right.
'''
def partA4Directions():
    # Read the maze file
    mazes = readMazeFromFile('pathfinding_a.txt')

    # Split each maze into its own list
    mazes = splitIntoSeparateMazes(mazes)
    count = 1
    # Loop through all the mazes in the list of lists
    for maze in mazes:
        # Loop through 2 times, once using A*, the other using Greedy
        for i in range(0, 2):
            # If i is 0 use A*
            if i == 0:
                # Create A* object
                alg = "A*"
                Grid = AStar4Directions()
            # I is 1, use Greedy
            else:
                alg = "GREEDY"
                Grid = Greedy4Directions()

            print("Running Part A, Maze " + str(count) + " with: " + alg)

            # initialize the maze
            Grid.initMaze(maze)

            # solve the maze
            pathList = Grid.findBestPath()

            # Check if we found a path, if we did, get the updated maze
            if pathList is not None:
                # Get the maze with the path added in as 'P'
                finalPath = getFinalPathAsList(Grid, pathList)

            # We did not find a path, make it the original maze with no changes
            else:
                finalPath = maze

            # Write the maze to a file
            writeMazeToFile(Grid.numRows, finalPath, alg, 'pathfinding_a_out.txt')
        count += 1


'''
Function: partB5Directions:
partB5Directions() is used for running part B of the assignment using up down left right and diagonal.
'''
def partB5Directions():
    # Read the maze file
    mazes = readMazeFromFile('pathfinding_b.txt')

    # Split each maze into its own list
    mazes = splitIntoSeparateMazes(mazes)
    count = 1

    # Loop through all the mazes in the list of lists
    for maze in mazes:
        # Loop through 2 times, once using A*, the other using Greedy
        for i in range(0, 2):
            # If i is 0 use A*
            if i == 0:
                # Create A* object
                alg = "A*"
                Grid = AStar5Directions()
            # I is 1, use Greedy
            else:
                alg = "GREEDY"
                Grid = Greedy5Directions()

            print("Running Part B, Maze " + str(count) + " with: " + alg)

            # initialize the maze
            Grid.initMaze(maze)

            # solve the maze
            pathList = Grid.findBestPath()

            # Check if we found a path, if we did, get the updated maze
            if pathList is not None:
                # Get the maze with the path added in as 'P'
                finalPath = getFinalPathAsList(Grid, pathList)

            # We did not find a path, make it the original maze with no changes
            else:
                finalPath = maze

            # Write the maze to a file
            writeMazeToFile(Grid.numRows, finalPath, alg, 'pathfinding_b_out.txt')
        count += 1


def main():
    #Runs 'part A.' of the assignment using up down left right
    print("Running Part A\n")
    partA4Directions()
    print("Done Part A\n\n")
    #RUNS 'part B.' of the assignment using up down left right diagonal
    print("Running Part B\n")
    partB5Directions()
    print("Done Part B\n")
    return


if __name__ == '__main__':
    main()
#import numpy as np
import random
# import sys
import time

MAX_SIZE_FOR_GRID_OUTPUT = 256
MAX_MOVES_BEFORE_RESTART = 2000
# MAX_RESTARTS_ALLOWED = 1000

#boardSizes = [4,32,64,125,256]

#todo: try... INSTEAD OF MOVING A CONFLICTING QUEEN RANDOMLY, COULD STORE NUMBER IT CONFLICTS WITH AND MOVE THE QUEEN WITH MOST CONFLICTS? MAYBE?

#read input from nqueens.txt, line by line
def readBoardSizesFromFile(filename):
  #read input from nqueens.txt, line by line
  #each line is an integer specifying board size (number of queens)

  # return [4, 32, 64, 125, 256]
  #return [500]

  with open(filename, 'r') as f:
    boardSizes = f.readlines()

  for i in range(len(boardSizes)):
    boardSizes[i] = int(boardSizes[i])

  return boardSizes


def displayBoardToConsole(size, board_0_based):
  #if n < 256, do visual form and 1-based matrix with queen locations, by row
  board_1_based = [x + 1 for x in board_0_based]

  if size < MAX_SIZE_FOR_GRID_OUTPUT:
    for row in range(size):
      for col in range(size):
        if col == board_0_based[row]:
          print "q ",
        else:
          print "x ",
      print "" # to get newline

  print (board_1_based)
  return


def writeBoardToFile(size, board_0_based, filename):

  #convert 0-based board to 1-based
  board_1_based = [x + 1 for x in board_0_based]

  # open file in appending mode
  with open(filename, 'a') as f:
    # if n < 256, do visual form and 1-based matrix with queen locations, by row
    if size < MAX_SIZE_FOR_GRID_OUTPUT:
      for row in range(size):
        for col in range(size):
          if col == board_0_based[row]:
            f.write("q ")
          else:
            f.write("x ")
        f.write("\n") # to get newline

    # print 1-based matrix representation
    f.writelines(str(board_1_based))
    f.write("\n\n")  # to get newline and skip a line between solutions
    f.close()

def updateQueensInConflict(size, board, queensInConflict, queensInCol, queensInDiagonalFromTopRight, queensInDiagonalFromTopLeft):

  for row in range (size):
    if board[row] == None:
      break
    else:
      col = board[row]
      numConflicts = queensInCol[col] + queensInDiagonalFromTopRight[row + col] + queensInDiagonalFromTopLeft[row + size - col - 1] - 3
      if numConflicts > 0:
        if [row, col] not in queensInConflict:
          queensInConflict.append([row, col])

  return queensInConflict

# returns the column within a row which would cause fewest conflicts if a queen were put there, updates queensInConflict array
def minConflictsWithinRow(size, queensInConflict, queensInCol, queensInDiagonalFromTopRight, queensInDiagonalFromTopLeft, row, oldColPosition):
  conflictsByColumn = [0] * size
  col = 0

  # if parameter "oldColPosition" is None, then there are no columns that are offlimit

  #check each col position in the row and count number of conflicts that would result from placing a queen there
  while col < size:

    if col == oldColPosition:
      conflictsByColumn[col] = size + 1 # set it to this so the old (off limits) column is never chosen. It would make no sense to move it to the same spot.
    else:
      numConflicts = queensInCol[col] + queensInDiagonalFromTopRight[row + col] + queensInDiagonalFromTopLeft[row + size - col - 1]
      if numConflicts == 0:
        bestCol = col
        break
      else:
        conflictsByColumn[col] = numConflicts
    col += 1

  if col == size:
    # no zero conflict position was found; choose column with least conflicts
    bestCol = conflictsByColumn.index(min(conflictsByColumn))

  return [queensInConflict, queensInCol, queensInDiagonalFromTopRight, queensInDiagonalFromTopLeft, row, bestCol]

def generateInitialBoard(size):
  #put each queen on its row/col so it conflicts with the fewest queens already on board
  #don't along multiple queens in a row, to avoid worst case scenarios
  #initial assignment: iterate through rows, and put queen where it has least conflicts with existing queens
  #maintain a list of queens that are in conflict, as well as total # of queens in each row, col and diagonal (i suppose there are 2 diagonals)

  #queensInDiagonalFromTopLeft            queensInDiagonalFromTopRight
  #       3 2 1 0                                      0 1 2 3
  #       4 3 2 1                                      1 2 3 4
  #       5 4 3 2                                      2 3 4 5
  #       6 5 4 3                                      3 4 5 6


  # initialize lists that will count number of queens in each col and diagonal
  queensInCol = [0] * size  # this array will contain the number of queens in each row
  queensInDiagonalFromTopRight = [0] * (2 * size - 1)  # number of queens in diagonal, bottomRight to topLeft
  queensInDiagonalFromTopLeft = [0] * (2 * size - 1)  # number of queens in diagonal, bottomLeft to topRight

  # initialize list to hold [row, col] of queens that are conflicting with at least one other queen on the board
  queensInConflict = []

  #for a cell (m, n) in a size*size grid, calculate the diagonal index:
  # diagonalFromTopRight = m + n
  # diagonalFromTopLeft = m + (size - n - 1)

  board = [None] * size #0-based matrix row by row, each location contains the col location of each queen

  for row in range(size):
    # calculate the number of conflicts for each column in that row
    # if find a col where placing a queen would generate 0 conflicts, place queen there.
    # otherwise, keep going for the whole column then choose a min index of the column

    [queensInConflict, queensInCol, queensInDiagonalFromTopRight, queensInDiagonalFromTopLeft, row, col] = \
      minConflictsWithinRow(size, queensInConflict, queensInCol, queensInDiagonalFromTopRight, queensInDiagonalFromTopLeft, row, None)

    board[row] = col
    queensInCol[col] += 1
    queensInDiagonalFromTopRight[row + col] += 1
    queensInDiagonalFromTopLeft[row + size - col - 1] += 1

    queensInConflict = updateQueensInConflict(size, board, queensInConflict, queensInCol, queensInDiagonalFromTopRight, queensInDiagonalFromTopLeft)


  return [board, queensInConflict, queensInCol, queensInDiagonalFromTopRight, queensInDiagonalFromTopLeft]


def solveWithIterativeRepair(size, board, queensInConflict, queensInCol, queensInDiagonalFromTopLeft, queensInDiagonalFromTopRight):

  numMoves = 0

  lastQueenMoved = [] # keep track of last queen moved so you don't accidentally randomly choose to move the same queen twice

  while (len(queensInConflict) > 0 and numMoves < MAX_MOVES_BEFORE_RESTART):
    #displayBoardToConsole(size, board)
    #print ("number of queens in conflict: " + str(len(queensInConflict)))
    #print(str(queensInConflict))
    #[row, oldColPosition] = random.choice(queensInConflict)


    [row, oldColPosition] = queensInConflict[random.randint(0, len(queensInConflict) -1)]

    # if queen randomly chosen is the queen that was moved in the last move, pick another random queen.
    # since it would be redundant to move the same queen twice in a row
    while ([row, oldColPosition] == lastQueenMoved):
      #print ("trying to fix queen in conflict at " + str([row, oldColPosition]))
      #print ("choose new queen; this one was moved last time")
      [row, oldColPosition] = queensInConflict[random.randint(0, len(queensInConflict) - 1)]

    queensInConflict.remove([row, oldColPosition])
    #print ("trying to fix queen in conflict at " + str([row, oldColPosition]))

    #check that the queen is still in conflict (conflict may have been result by previous queens moved)
    numConflicts = queensInCol[oldColPosition] + queensInDiagonalFromTopRight[row + oldColPosition] \
                   + queensInDiagonalFromTopLeft[row + size - oldColPosition - 1] - 3 #subtract 3 for queen you just removed

    if numConflicts == 0:
      # just remove it from queensInConflict list; don't count this as a move
      numMoves -=1

    #print ("this queen has " + str(numConflicts) + " conflicts")
    if numConflicts > 0:
      # remove conflicting queen; update counters for number of queens in each col and diagonal
      queensInCol[oldColPosition] -= 1
      queensInDiagonalFromTopRight[row + oldColPosition] -= 1
      queensInDiagonalFromTopLeft[row + size - oldColPosition - 1] -= 1

      # find which col you could move it to that would have least conflicts
      [queensInConflict, queensInCol, queensInDiagonalFromTopRight, queensInDiagonalFromTopLeft, row, newColPosition] = \
        minConflictsWithinRow(size, queensInConflict, queensInCol, queensInDiagonalFromTopRight, queensInDiagonalFromTopLeft, row, oldColPosition)

      #print ("best (min conflict) place to move it is " + str([row, newColPosition]))

      #place queen at new column with the row; update board, and update counters for number of queens in each col and diagonal
      board [row] = newColPosition
      queensInCol[newColPosition] += 1
      queensInDiagonalFromTopRight[row + newColPosition] += 1
      queensInDiagonalFromTopLeft[row + size - newColPosition - 1] += 1

      # numConflicts = queensInCol[newColPosition] + queensInDiagonalFromTopRight[row + newColPosition] \
      #                + queensInDiagonalFromTopLeft[row + size - newColPosition - 1] - 3
      #
      # if numConflicts > 0:
      #   if [row, newColPosition] not in queensInConflict:
      #     queensInConflict.append([row, newColPosition])

      queensInConflict = updateQueensInConflict(size, board, queensInConflict, queensInCol, queensInDiagonalFromTopRight, queensInDiagonalFromTopLeft)
      #queensInConflict = removeQueensNoLongerInConflict(size, board, queensInConflict, queensInCol, queensInDiagonalFromTopLeft, queensInDiagonalFromTopRight)


      lastQueenMoved = [row, newColPosition]


    numMoves += 1
    #print ("move # " + str(numMoves))


  if numMoves == MAX_MOVES_BEFORE_RESTART:
    print ("Hit max num moves. Triggering restart. Queens still in conflict: " + str(queensInConflict))
    return False

  print ("num repairs: " + str(numMoves))

  return board

def checkThatFinalBoardHasNoConflicts(size, board):

  # check that no col or diagonal contains > 1 queen

  queensPerDiagonalFromTopRight = [0] * (2 * size - 1)
  queensPerDiagonalFromTopLeft = [0] * (2 * size - 1)
  queensPerColumn = [0] * size

  for row in range(size):
    col = board[row]
    queensPerColumn[col] += 1
    if queensPerColumn[col] > 1:
      print ("FAIL. Some column contains > 1 queen.")
      return False

    queensPerDiagonalFromTopRight[row + col] += 1
    if queensPerDiagonalFromTopRight[row + col] > 1:
      print ("FAIL. Some diagonal from top right contains > 1 queen.")
      return False

    queensPerDiagonalFromTopLeft [row + size - col - 1] += 1
    if queensPerDiagonalFromTopLeft [row + size - col - 1] > 1:
      print ("FAIL. Some diagonal from top left contains > 1 queen.")
      return False

  # for a cell (m, n) in a size*size grid, calculate the diagonal index:
  # diagonalFromTopRight = m + n
  # diagonalFromTopLeft = m + (size - n - 1)

  print ("Final board has no conflicts. Yay!")
  return True


def main():
  inFileName = "nqueens.txt"
  outFileName = "nqueens_out.txt"
  boardSizes = readBoardSizesFromFile(inFileName)

  for size in boardSizes:

    print ("starting the " + str(size) + "-queens problem")
    startTime = time.time()
    print("start time: " + str(time.ctime()))

    print ("repairing to get final board...")
    # fix the n-queens board using iterative repair
    finalBoard = False
    numRestarts = -1
    while finalBoard == False:
      numRestarts += 1

      # generate initial board (one queen per column, queens positioned to minimize number of conflicts as the board is created)
      [initialBoard, queensInConflict, queensInCol, queensInDiagonalFromTopRight,
       queensInDiagonalFromTopLeft] = generateInitialBoard(size)
      print ("Restart #" + str(numRestarts + 1) + ") initial conflicts..." + str(queensInConflict))

      finalBoard = solveWithIterativeRepair(size, initialBoard, queensInConflict, queensInCol, queensInDiagonalFromTopLeft, queensInDiagonalFromTopRight)

      # if numRestarts == MAX_RESTARTS_ALLOWED: #  PROBABLY REMOVE THIS WHEN
      #   print ("Hit " + str(MAX_RESTARTS_ALLOWED) + " restarts, will stop now.")
      #   break

    checkThatFinalBoardHasNoConflicts(size, finalBoard) # can remove this later

    writeBoardToFile(size, initialBoard, outFileName)
    displayBoardToConsole(size, finalBoard)
    print ("num restarts: " + str(numRestarts))
    elapsedTime = time.time() - startTime
    print ("elapsed time: " + str(int(elapsedTime / 60)) + " min " + str(elapsedTime % 60) + " s")

  return


if __name__ == '__main__':
  main()

#solutions are not unique
#the min-conflicts alg is not guaranteed to find a solution;
#if no sol'n (if it loops) need to restart algorithm with a new initial board configuration
#and repeat until sol'n found
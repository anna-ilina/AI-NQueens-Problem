#import numpy as np
import random
import sys

MAX_SIZE_FOR_GRID_OUTPUT = 256

#boardSizes = [4,32,64,125,256]
boardSizes = 4

#read input from nqueens.txt, line by line
def readBoardSizesFromFile(filename):
  #read input from nqueens.txt, line by line
  #each line is an integer specifying board size (number of queens)
  # return [4, 32, 64, 125, 256]
  return [4]

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


# # open the file for appending
# with open(filename, 'a') as f:
#   # write the alg used
#   f.write(alg + "\n")
#   # prints the maze into the file in proper format
#   for i in range(numRows):
#     f.writelines(finalPath[i])
#     f.write("\n")
#   # Blank line to separate after Greedy
#   if alg == "GREEDY":
#     f.write("\n")
# # close file
# print("Ouput saved in " + filename)
# f.close()


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
    f.write("\n")  # to get newline
    f.close()

def generateInitialBoard(size):
  #put each queen on its row/col so it conflicts with the fewest queens already on board
  #don't along multiple queens in a row, to avoid worst case scenarios
  #initial assignment: iterate through rows, and put queen where it has least conflicts with existing queens
  #maintain a list of queens that are in conflict, as well as total # of queens in each row, col and diagonal (i suppose there are 2 diagonals)

  #Rather than scanning a row for the position with the fewest conflicts, the optimized program maintains a list of
  # empty columns (which tends to be quite small); it first checks for a zero-conflict position by looking for an
  # empty column with no conflicts along the diagonals.If there is no zero-conflict position, the program repeatedly
  # looks for a position with one conflict by randomly selecting a position and checking the number of conflicts in
  # that  position.Since there tend to be many positions with  one conflict, this technique tends to succeed after
  # just a few tries, so the total number of positions examined is generally very low.

  #queensInDiagonalFromTopLeft            queensInDiagonalFromTopRight
  #       3 2 1 0                                      0 1 2 3
  #       4 3 2 1                                      1 2 3 4
  #       5 4 3 2                                      2 3 4 5
  #       6 5 4 3                                      3 4 5 6

  queensInCol = [0] * size # this array will contain the number of queens in each row
  queensInDiagonalFromTopRight = [0] * (2*size -1) # number of queens in diagonal, bottomRight to topLeft
  queensInDiagonalFromTopLeft = [0] * (2*size -1) # number of queens in diagonal, bottomLeft to topRight
  #for a cell (m, n) in a size*size grid, calculate the diagonal index:
  # diagonalFromTopRight = m + n
  # diagonalFromTopLeft = m + (size - n - 1)

  board = [None] * size #0-based matrix row by row, each location contains the col location of each queen

  for row in range(size):
    # calculate the number of conflicts for each column in that row
    # if find a col where placing a queen would generate 0 conflicts, place queen there.
    # otherwise, keep going for the whole column then choose a min index of the column

    conflictsByColumn = [0] * size
    col = 0
    while col < size:

      # print ("for [row,col] = ")
      # print(row)
      # print(col)
      # print ("queensInCol = ", queensInCol[col])
      # print("queensInDiagonalFromTopRight = " , queensInDiagonalFromTopRight[row + col])
      # print ("queensinDiagonalFromTopLeft = " , queensInDiagonalFromTopLeft[row + size - col - 1])

      numConflicts = queensInCol[col] + queensInDiagonalFromTopRight[row + col] + queensInDiagonalFromTopLeft[row + size - col - 1]
      # print ("numConflicts = " + str(numConflicts))
      if numConflicts == 0:
        break
      else:
        conflictsByColumn[col] = numConflicts
        col += 1

    if col ==  size:
      #no zero conflict position was found; choose column with least conflicts
      col = conflictsByColumn.index(min(conflictsByColumn))

    #place the queen at location [row, col] and update conflicts counters accordingly
    # print ("placed queen at location [row, col]")
    # print (row)
    # print (col)

    board [row] = col
    queensInCol[col] += 1
    queensInDiagonalFromTopRight[row + col] += 1
    queensInDiagonalFromTopLeft[row + size - col - 1] += 1

  return board

def countConflicts (size, board, rowToAddQueen):
  return

def minConflicts(size, board, currentRow):
  return

def solveWithIterativeRepair(size, board):
  return

def main():
  inFileName = "nqueens.txt"
  outFileName = "nqueens_out.txt"
  boardSizes = readBoardSizesFromFile(inFileName)
  for size in boardSizes:
    initialBoard = generateInitialBoard(size)
    displayBoardToConsole(size, initialBoard)
    writeBoardToFile(size, initialBoard, outFileName)

  return

if __name__ == '__main__':
  main()
  
#solutions are not unique
#the min-conflicts alg is not guaranteed to find a solution;
#if no sol'n (if it loops) need to restart algorithm with a new initial board configuration
#and repeat until sol'n found
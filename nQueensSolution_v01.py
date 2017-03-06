#read input from nqueens.txt, line by line

#boardSizes = [4,32,64,125,256]
boardSizes = 4

def readBoardSizesFromFile(filename):
  #read input from nqueens.txt, line by line
  #each line is an integer specifying board size (number of queens)
  # return [4, 32, 64, 125, 256]
  return [4]

def displayBoard(size, board):
  #output to nqueens_out.txt
  #if n < 256, do visual form and 1-based matrix with queen locations, by row
  return

def generateInitialBoard(size):
  #put each queen on its row/col so it conflicts with the fewest queens already on board
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
    generateInitialBoard(size)

#solutions are not unique
#the min-conflicts alg is not guaranteed to find a solution;
#if no sol'n (if it loops) need to restart algorithm with a new initial board configuration
#and repeat until sol'n found
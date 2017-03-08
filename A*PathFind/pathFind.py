'''
Cisc 352 Assignment 3

Justin Gerolami - 10160479 - 14JG28
Anna Ilina - -
'''

import itertools

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


def main():
    mazes = readMazeFromFile()
    #print(mazes)
    mazes = splitIntoSeparateMazes(mazes)
    print(mazes)

if __name__ == '__main__':
    main()

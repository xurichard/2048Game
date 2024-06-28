# You are most likely familiar with the game 2048.

# 2048 is played on a gray 4x4 grid with numbered tiles that slide smoothly 
# when a player moves them using one of the four arrow keys - Up, Down, Left or 
# Right. On every turn, a new tile with a value of either 2 or 4 randomly 
# appears on an empty spot of the board. After one of the keys is pressed, the 
# tiles slide as far as possible in the chosen direction until they are stopped 
# either by another tile or by the edge of the grid. If two tiles with the same 
# number collide while moving, they merge into a tile with this number doubled. 
# You can't merge an already merged tile in the same turn. If there are more than 
# 2 tiles in the same row (column) that can merge, the farthest 
# (closest to an edge) pair will be merged first (see the second example).

# In this problem you are not going to solve the 2048 puzzle, but you are going 
# to find the final state of the board from the given one after a defined set of 
# n arrow key presses, assuming that no new random tiles will appear on the empty 
# spots.

# You are given a matrix 4x4 which corresponds to the 2048 game grid. grid[0][0] 
# corresponds to the upper left tile of the grid. Each element of the grid is 
# equal to some power of 2 if there is a tile with that value in the corresponding 
# position, and 0 if it corresponds to the empty spot. You are also given a 
# sequence of key presses as a string path. Each character of the string equals 
# L, R, U, or D corresponding to Left, Right, Up or Down respectively.

# Please note that in some cases after pressing an arrow key nothing will be 
# changed.

# Example
# For

# grid = [[0, 0, 0, 0],
#         [0, 0, 2, 2],
#         [0, 0, 2, 4],
#         [2, 2, 4, 8]]
# and path = "RR"

# the output should be

# game2048(grid, path) = [[0, 0, 0, 0],
#                         [0, 0, 0, 4],
#                         [0, 0, 2, 4],
#                         [0, 0, 8, 8]]

# rotate a matrix clockwise
# def rotate(matrix):
#         (i,j) -> (n-i-1, n-j-1)

#         (0,0) -> (3,0)
#         (0,1) -> (3,2)
#         (3,3) -> (0,3)

# reference: https://codereview.stackexchange.com/questions/179276/codefights-game-2048?fbclid=IwAR3XqU02M10oK1w2eM37aeShxbneYB_D2n_UeMQh_WeN2wA5JSaAWwOqYY8

import unittest
import random

# one liner for rotating nxn matrix clockwise
def rotateMatrixClockwise(matrix):
    return zip(*grid[::-1])


class Game2048:
    def __init__(self, size):
        self.size = size
        self.board = [[0 for i in range(size)] for j in range(size)]
        self.score = 0

    def setupBoard(self):
        for i in range(2):
            emptySpaces = self.getEmptySpace()
            space = emptySpaces[random.randrange(len(emptySpaces))]
            self.board[space[0]][space[1]] = 2<<random.randrange(3)

    def reset(self):
        self.board = [[0 for i in range(4)] for j in range(4)]
        self.score = 0
        self.setupBoard()

    # in place merges the column by using 2 pointers where i points to the original
    # column items we're comparing and j points to where it falls into the next state

    # Assumes that the 0th index is the direction we're merging into
    # [2,4,8,16], merging <- that way

    # returns false if the col didn't change and true if it did
    def mergeOneColumn(self, col):
        lastNonzeroIndex = -1
        trailingZerosCheck = False
        i = 0
        j = 0
        while i < len(col):
            if col[i] == 0:
                i+=1
            else:
                # I'm not going to do a sanity check for it being an exponent of 2
                # if col[i+1] == 0, we have to check if the next nonzero element is
                # the same as col[i]
                lastNonzeroIndex = i
                while i < len(col) - 1 and col[i+1] == 0:
                    i+=1

                if i >= len(col)-1:
                    # the rest of the list was 0
                    col[j] = col[lastNonzeroIndex]
                    # we need a specific check for trailing zeros to avoid confusion
                    # with trailling 0s after a merge
                    # if we have a unique number with trailling 0s until the end of
                    # col, if j == lastNonzeroIndex, no merges have happened before
                    # this distringushes between [2,0,0,0] and [2,2,0,0]
                    if j == lastNonzeroIndex:
                        trailingZerosCheck = True
                    # increment j to be consistent with other cases so we can 
                    # start appending 0s starting at j
                    i+=1
                elif col[lastNonzeroIndex] == col[i+1]:
                    col[j] = col[lastNonzeroIndex] + col[i+1]
                    self.score += col[j]
                    i+=2
                else:
                    col[j] = col[lastNonzeroIndex]
                    i+=1
                j+=1

        # 1. i and j can only be the same if all elements were the same, there is no
        #    way for j to update without i making the same update
        # so if i and j differ, we have to know it's not because of trailing 0s
        # 2. the trailingZerosCheck is false to represent the nonZero elements were
        #    not equal before the 0s
        # 3. check for if the entire col is 0s
        changed = False
        if j != i and not trailingZerosCheck and lastNonzeroIndex != -1:
            changed = True

        # fill in the 0s at the end 
        while j < len(col):
            col[j] = 0
            j+=1

        return changed


    # Takes each column of the board in order and copy it over to an array
    # do the merge on each column individually and copy it back over to the array
    # returns True if the board state changed, false if the board state didn't
    def mergeBoard(self, direction):
        changed = False
        if direction == "R":
            for r in range(len(self.board)):
                tempCol = self.board[r][::-1]
                rowChanged = self.mergeOneColumn(tempCol)
                changed = changed or rowChanged
                self.board[r] = tempCol[::-1]
        elif direction == "L":
            for r in self.board:
                rowChanged = self.mergeOneColumn(r)
                changed = changed or rowChanged
        elif direction == "U":
            for c in range(len(self.board[0])):
                tempCol = [None] * len(self.board[0])
                for r in range(len(self.board)):
                    tempCol[r] = self.board[r][c]
                rowChanged = self.mergeOneColumn(tempCol)
                changed = changed or rowChanged
                for r in range(len(self.board)):
                    self.board[r][c] = tempCol[r]
        elif direction == "D":
            for c in range(len(self.board[0])):
                tempCol = [None] * len(self.board[0])
                for r in range(len(self.board)):
                    tempCol[r] = self.board[len(self.board) - 1 - r][c]
                rowChanged = self.mergeOneColumn(tempCol)
                changed = changed or rowChanged
                for r in range(len(self.board)):
                    self.board[len(tempCol) - 1 - r][c] = tempCol[r]
        return changed


    # updates the board to the next state including merging elements and 
    # adding a random element
    def nextState(self, direction):
        changed = self.mergeBoard(direction)
        if changed:
            emptySpaces = self.getEmptySpace()
            space = emptySpaces[random.randrange(len(emptySpaces))]
            self.board[space[0]][space[1]] = 2<<random.randrange(3)

        return changed


    # TODO(richardxu): optimize by creating a global list or dict of empty spots
    #                  updated by mergeOneColumn, should avoid the O(n^2) operation
    #                  of searching the board every time
    def getEmptySpace(self):
        emptySpaces = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c] == 0:
                    emptySpaces.append((r,c))
        return emptySpaces


    # starting from the top right, you can check each elements lower and right 
    # neighbors. We can ignore an element's upper and left neighbor because we 
    # know that both those neighbors have checked the element itself.

    # TODO(richardxu): To optimize, figure out if we can look at the last element
    # added + neighbors to see if the board state is locked
    def lockedBoardState(self):
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c] == 0:
                    return False
                for neighbor in [(1,0), (0,-1)]: # check right and down
                    nr = r+neighbor[0]
                    nc = c+neighbor[1]
                    if 0 <= nr < len(self.board) and 0 <= nc < len(self.board[r]) and \
                        self.board[r][c] == self.board[nr][nc]: # valid space
                        return False
        return True

    # prints board to console out
    def printBoard(self):
        print("--------------------------------------------------------")
        print("Score: ", self.score)

        s = [[str(e) for e in row] for row in self.board]
        lens = [max(map(len, col)) for col in zip(*s)]
        max_lens = [max(lens)]*len(self.board)
        fmt = ' '.join('{{:^{}}}'.format(x) for x in max_lens)
        table = [fmt.format(*row) for row in s]
        print('\n'.join(table))


if __name__ == '__main__':
    game = Game2048(4)
    game.setupBoard()

    val = "temp"
    while val.lower():
        # display board
        game.printBoard()

        # get user input
        val = input("Enter a direction or quit: ")
        if val.lower() == "quit":
            print("Thanks for playing!")
            break
        elif val.upper() in ["R", "L", "U", "D"]:
            changed = game.nextState(val.upper())

            if game.lockedBoardState():
                print("Game Over")
                game.printBoard()
                break
        else:
            print("invalid input, try again.")
            continue




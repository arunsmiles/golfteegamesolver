from os import error
import copy
from collections import namedtuple
Move = namedtuple('Move', ['fromIndex', 'overIndex', 'toIndex'])
Index = namedtuple('Index', ['row', 'col'])

def printGolfTee(golfTee):
    for onedArray in golfTee:
        line = ""
        for element in onedArray:
            if element == '':
                line += '   '
            else:
                line += ' ' + element + ' '

        print(line)

def getGolfTeeState(golfTee, idx):
    if idx.row < len(golfTee) and idx.col < len(golfTee[idx.row]) and golfTee[idx.row][idx.col] != '':
        return golfTee[idx.row][idx.col]

def setGolfTeeState(golfTee, idx, value):
    currentState = getGolfTeeState(golfTee, idx)
    if currentState == '0' or currentState == '1':
        golfTee[idx.row][idx.col] = value
    else:
        error("Can't update state of index ", idx)

def getBottomLeftIndex(idx):
    return Index(idx.row+2, idx.col-1)

def getBottomRightIndex(idx):
    return Index(idx.row+2, idx.col+1)

def getLeftIndex(idx):
    return Index(idx.row, idx.col-2)

def getRightIndex(idx):
    return Index(idx.row, idx.col+2)

def getTopRightIndex(idx):
    return Index(idx.row-2, idx.col+1)

def getTopLeftIndex(idx):
    return Index(idx.row-2, idx.col-1)

def getBottomLeft(golfTee, idx):
    return getGolfTeeState(golfTee, getBottomLeftIndex(idx))

def getBottomRight(golfTee, idx):
    return getGolfTeeState(golfTee, getBottomRightIndex(idx))

def getLeft(golfTee, idx):
    return getGolfTeeState(golfTee, getLeftIndex(idx))

def getRight(golfTee, idx):
    return getGolfTeeState(golfTee, getRightIndex(idx))

def getTopLeft(golfTee, idx):
    return getGolfTeeState(golfTee, getTopLeftIndex(idx))

def getTopRight(golfTee, idx):
    return getGolfTeeState(golfTee, getTopRightIndex(idx))

def getReadableIndex(index):
    c = index.col
    if c%2 == 0:
        c -= 1
    return "{},{}".format((index.row + 1)/2 + 1, (c+1)/2-(9-index.row)/4 + 1)

def printMove(move):
    print ("Move from {} to {}".format(getReadableIndex(move.fromIndex), getReadableIndex(move.toIndex)))

def getPossibleMovesOver(overIndex):
    return [
    Move(getBottomRightIndex(overIndex), overIndex, getTopLeftIndex(overIndex)),
    Move(getTopLeftIndex(overIndex), overIndex, getBottomRightIndex(overIndex)),
    Move(getLeftIndex(overIndex), overIndex, getRightIndex(overIndex)),
    Move(getRightIndex(overIndex), overIndex, getLeftIndex(overIndex)),
    Move(getBottomLeftIndex(overIndex), overIndex, getTopRightIndex(overIndex)),
    Move(getTopRightIndex(overIndex), overIndex, getBottomLeftIndex(overIndex))
    ]

def canMakeMove(golfTee, move):
    if getGolfTeeState(golfTee, move.fromIndex) != '1' or getGolfTeeState(golfTee, move.overIndex) != '1' or getGolfTeeState(golfTee, move.toIndex) != '0':
        return False
    return True

def makeMove(golfTee, move):
    if canMakeMove(golfTee, move):
        setGolfTeeState(golfTee, move.fromIndex, '0')
        setGolfTeeState(golfTee, move.overIndex, '0')
        setGolfTeeState(golfTee, move.toIndex, '1')
    else:
        error("Can't make move ", move)

def isTargetState(golfTee):
    count = 0
    for row in golfTee:
        for element in row:
            if element == '1':
                count += 1
    if count == 1:
        return True
    return False

def getMovesToWin(golfTee):
    if isTargetState(golfTee):
        return []
    for i in range(len(golfTee)):
        for j in range(len(golfTee[i])):
            if golfTee[i][j] == '1':
                for move in getPossibleMovesOver(Index(i, j)):
                    if canMakeMove(golfTee, move):
                        golfTeeCopy = copy.deepcopy(golfTee)
                        makeMove(golfTeeCopy, move)
                        movesToWin = getMovesToWin(golfTeeCopy)
                        if movesToWin != None:
                            movesToWin.insert(0, move)
                            return movesToWin

golfTee = [
            ['', '', '', '', '0', '', '', '', ''],
            ['', '', '', '', '', '', '', '', ''],
            ['', '', '', '1', '', '1', '', '', ''],
            ['', '', '', '', '', '', '', '', ''],
            ['', '', '1', '', '1', '', '1', '', ''],
            ['', '', '', '', '', '', '', '', ''],
            ['', '1', '', '1', '', '1', '', '1', ''],
            ['', '', '', '', '', '', '', '', ''],
            ['1', '', '1', '', '1', '', '1', '', '1']
             ]

printGolfTee(golfTee)

movesToWin = getMovesToWin(golfTee)
for move in movesToWin:
    printMove(move)
    makeMove(golfTee, move)
    printGolfTee(golfTee)

print("Summary of moves to win:")
for move in movesToWin:
    printMove(move)


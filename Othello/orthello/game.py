import copy
EMPTY, BLACK, WHITE = '.', '●', '○'
HUMAN, COMPUTER = '●', '○'

UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)
VIC=10000000 #The value of a winning board (for max)
LOSS=-VIC #The value of a losing board (for max)
TIE=0 #The value of a tie

'''
The state of the game is represented by a list of 4 items:
0. The game board - a matrix (list of lists) of ints. Empty cells = 0,
   the comp's cells = COMPUTER and the human's = HUMAN
1. The heuristic value of the state.
2. Who's turn is it: HUMAN or COMPUTER
3. flag to end game

'''

#The user decides who plays first
def whoIsFirst(s):
    global HUMAN,COMPUTER
    firstPlayer = input("Who goes first? Type human or computer ")

    if (firstPlayer == "human"):
        s[2]=HUMAN 
    elif (firstPlayer == "computer"):
        HUMAN, COMPUTER = '○', '●' #because black always goes first
        s[2]=COMPUTER 
    #note: if you type in something besides human or computer, you are going to go first
    return s

def isHumTurn(s):
#Returns True iff it the human's turn to play
    return s[2]==HUMAN

def squares():
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]

#The HUMAN plays first (=BLACK)
def create():
    global HUMAN,COMPUTER
    board = [EMPTY] * 100
    for i in squares():
        board[i] = EMPTY
    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    HUMAN, COMPUTER = '●', '○'
    return [board,0.00001, HUMAN,False]

def createLateStageBoard(): #simply for testing purposes
    global HUMAN,COMPUTER
    board = [EMPTY] * 100
    for i in squares():
        #print(i)
        if(i % 2 == 0):
            board[i] = WHITE
            #print("white")
        else:
            board[i] = BLACK
            #print("black")

    board[64], board[87] = EMPTY, EMPTY
    board[43], board[21] = EMPTY, EMPTY
    HUMAN, COMPUTER = '●', '○'
    return [board,0.00001, HUMAN,False]



def printState(s):
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    for row in range(1, 9):
        begin, end = 10*row + 1, 10*row + 9
        rep += '%d %s\n' % (row, ' '.join(s[0][begin:end]))
    print(rep)

    if s[1] == VIC:
        print("Ha ha ha I won!")
    elif s[1] == LOSS:
        print("You did it!")
    elif s[1] == TIE:
        print("It's a TIE")

def inputMove(s):
# Reads, enforces legality and executes the user's move.

    flag=True
    while flag:
        printState(s)
        move=int(input("To make your move enter a two digits number, the first number is row and the second is column" "\n" \
        "For example: if you want to choose the first row and the third column enter 13" "\n"\
        "Enter your next move: "))
        if isLegal(move, s) ==False:
            print("Illegal move.")
        else:
            flag=False
            makeMove(move,s)


def value(s):
#Returns the heuristic value of s
        s[1]=1  ### your code here ###
        board = s[0]
        heuristic = 0
        top_left = board[11]
        top_right = board[18] 
        bottom_left = board[81]
        bottom_right = board[88]
        corners = [top_left, top_right, bottom_left, bottom_right]

        #+30 points for every corner it has and -30 points for every corner human has
        for corner in corners:
            if corner == COMPUTER:
                heuristic += 30
            if corner == HUMAN:
                heuristic -= 30
        
        #defining edges. Does not count corners because those were already counted, and also does not count the square right next to a corner because that could be very dangerous as it allows access to the corner
        firstRow = [board[n] for n in range(13,17)] 
        firstCol = [board[n] for n in range(31, 71, 10)]
        lastRow = [board[n] for n in range(83, 87)]
        lastCol = [board[n] for n in range(38, 78, 10)]

        edges = [firstRow, firstCol, lastRow, lastCol]

        # I defined edge squares to be worth four points (as opposed to the corners which were worth 30)
        for edge in edges:
            for square in edge:
                if square == COMPUTER:
                    heuristic += 4
                if square == HUMAN:
                    heuristic -= 4


        currentPlayer = s[2]
        s[2] = COMPUTER #temporarily making sure current player is computer to easily calculate the number of moves it has available on the board
        #My thinking here is the more moves the computer can make the better the position is for it
        heuristic += 2 * len(legalMoves(s)) 

        s[2] = HUMAN
        heuristic -= 2 * len(legalMoves(s)) #doing the same thing but subtracting points for the amount of moves the human has available

        s[2] = currentPlayer #setting player back to what it was supposed to be

        if len(legalMoves(s)) == 0: #this state represents a game that is over
            computerScore=0
            humanScore=0
            for sq in squares():
                piece = s[0][sq]
                if piece == COMPUTER:
                    computerScore += 1
                elif piece == HUMAN:
                    humanScore += 1
#the only thing that matters in a game that has ended is who won
#large positive heuristic if computer wins, large negative if computer loses
            if (computerScore>humanScore):
                heuristic = 100000
            if (computerScore<humanScore):
                heuristic = -100000




        if heuristic == 0:
                # if I returned this it would accidentally signal that the game has ended in a state of TIE
                heuristic = .0001
        s[1] = heuristic      

        return s[1]



def isFinished(s):
#Returns True if the game ended

    ### your code here ###
    if (len(legalMoves(s)) == 0): #current player can not go
        s[3] = True #game is over
        s[1] = whoWin(s) #store who won in the state
    return (s[3]) 

def isLegal(move, s):
    hasbracket = lambda direction: findBracket(move, s, direction)
    return s[0][move] == EMPTY and any(map(hasbracket, DIRECTIONS))

# get a list of legal moves for the player
def legalMoves(s):
    return [sq for sq in squares() if isLegal(sq, s)]

# Is there any legal move for this player
def anyLegalMove(s):
    isAny = any(isLegal(sq, s) for sq in squares())
    if (not(isAny)):
        s[3] = True
    return isAny

def makeFlips(move, s, direction):
    bracket = findBracket(move, s, direction)
    if not bracket:
        return
    square = move + direction
    while square != bracket:
        s[0][square] = s[2]
        square += direction

def changePlayer(s):
    if s[2] == COMPUTER:
            s[2] = HUMAN
    else:
       s[2] = COMPUTER

def makeMove(move, s):
    s[0][move] = s[2]
    for d in DIRECTIONS:
        makeFlips(move, s, d)
    value(s)
    changePlayer (s)
    return s

def whoWin (s):
    computerScore=0
    humanScore=0
    for sq in squares():
        piece = s[0][sq]
        if piece == COMPUTER:
            computerScore += 1
        elif piece == HUMAN:
            humanScore += 1
    if (computerScore>humanScore):
        return VIC

    elif (computerScore<humanScore):
        return LOSS

    elif (computerScore==HUMAN):
        return TIE

    return 0.00001 #not 0 because TIE is 0


def isValid(move):
    return isinstance(move, int) and move in squares()

def findBracket(square, s, direction):
    bracket = square + direction
    if s[0][bracket] == s[2]:
        return None
    opp = BLACK if s[2] is WHITE else WHITE
    while s[0][bracket] == opp:
        bracket += direction
    return None if s[0][bracket] in (EMPTY) else bracket

def getNext(s):
# returns a list of the next states of s
    ns=[]
    for m in legalMoves(s):
        tmp=copy.deepcopy(s)
        makeMove(m,tmp)
        ns+=[tmp]
    return ns


# def createBoardWithVal():
#     global HUMAN,COMPUTER
#     board = [EMPTY] * 100
#     HUMAN, COMPUTER = '●', '○'
#     board[13] = HUMAN
#     board[14] = COMPUTER
#     board[88] = HUMAN
#     board[11] = HUMAN
#     board[12] = HUMAN
#     board[44], board[45] = WHITE, BLACK
#     board[54], board[55] = BLACK, WHITE
#     return [board,0.00001, HUMAN,False]
# printState(createBoardWithVal())

# print(value(createBoardWithVal()))
# quit()
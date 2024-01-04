import csv
import time
columns = [] #columns is the locations for each of the queens
# columns[r] is a number c if a queen is placed at row r and column c.
size = 10


import random #hint -- you will need this for the following code: column=random.randrange(0,size)

def place_n_queens(size):
    columns.clear()
    row = 0
    while row < size:
        column=random.randrange(0,size)
        columns.append(column)
        row+=1


def display():
    for row in range(len(columns)):
        for column in range(size):
            if column == columns[row]:
                print('♛', end=' ')
            else:
                print(' .', end=' ')
        print()




def propogate(row, column, illegalColumns): #I placed a queen in this row and column and now I will propogate forward so I know which places are illegal
    #the idea here is that illegalColumns[i] lists the columns that a queen in row i cannot be placed into
    for i in range(row + 1, size):
        illegalColumns[i].add(column)

    for queen_row in range(row+1, size):
        for queen_column in range(0, size):
            if queen_column - queen_row == column - row:
                illegalColumns[queen_row].add(queen_column)
            
            if ((size - queen_column) - queen_row == (size - column) - row):
                illegalColumns[queen_row].add(queen_column)





def dfs_solve_queen(size, forwardPropogate): #forwardPropogate is always true in this file
    tic = time.time()
    illegalColumns = [set() for n in range(size)] #When I place a queen I will propgogate by filling in the now illegal columns for each row

    stackOfIllegalColumns = [] #stack so when I backtrack I can return to the previous list of illegal columns
    stackOfIllegalColumns.append(illegalColumns)
    columns.clear()
    number_of_moves = 0 
    number_of_iterations = 0
    row = 0
    column = 0
    smartBackTrack = False #smart back track means there's a future row where every column is illegal, so I should backtrack now
    # iterate over rows of board
    while True:
        while column < size:
            number_of_iterations+=1
            if column not in illegalColumns[row]:               
                place_in_next_row(column)
                number_of_moves += 1
                if forwardPropogate: #For this file this will always be true
                    stackOfIllegalColumns.append(illegalColumns) #save previous state of illegalColumns
                    illegalColumns = [set(n) for n in stackOfIllegalColumns[-1]] #make new copy of illegalColumns
                    propogate(row, column, illegalColumns) #propogate the change from the move I just made
                    #print("here is illegalColumns", illegalColumns)
                    if column < size: #sanity check
                        for n in range(row, len(illegalColumns)):
                            #Almost positive I don't need to do iterations++ in the for loop here: I'm just checking the length of each set in illegal columns to see if I should backtrack
                            if len(illegalColumns[n]) == size: #there is a future row where I will not be able to place a queen
                                smartBackTrack = True #so backtrack now
                                break


                row += 1
                column = 0
                break
            else:
                column += 1
        # if I could not find an open column or if board is full or smartBackTrack
        if (column == size or row == size or smartBackTrack):
            smartBackTrack = False
            number_of_iterations+=1
            # if board is full, we have a solution
            if row == size:
                # print("I did it! Here is my solution")
                # display()
                #print(number_of_moves)
                return number_of_iterations, number_of_moves, time.time() - tic
            # I couldn't find a solution so I now backtrack
            prev_column = remove_in_current_row()
            number_of_moves += 1
            illegalColumns = stackOfIllegalColumns.pop() # go back to previous version of illegalColumns
            if (prev_column == -1): #I backtracked past column 1
                print("There are no solutions")
                #print(number_of_moves)
                return number_of_iterations, number_of_moves, time.time() - tic
            # try previous row again
            row -= 1
            # start checking at column = (1 + value of column in previous row)
            column = 1 + prev_column


def place_in_next_row(column):
    columns.append(column)

def remove_in_current_row():
    if len(columns) > 0:
        return columns.pop()
    return -1

def next_row_is_safe(column):
    row = len(columns)
    # check column
    for queen_column in columns:
        if column == queen_column:
            return False

    # check diagonal
    for queen_row, queen_column in enumerate(columns):
        if queen_column - queen_row == column - row:
            return False

    # check other diagonal
    for queen_row, queen_column in enumerate(columns):
        if ((size - queen_column) - queen_row
            == (size - column) - row):
            return False
    return True



def countConflicts(): #I don't use this method in this file at all
    conflictsArray = []
    for row, column in enumerate(columns):
        conflicts = 0
            # check column
        for queen_column in columns:
            if column == queen_column:
                conflicts+=1

        # check diagonal
        for queen_row, queen_column in enumerate(columns):
            if queen_column - queen_row == column - row:
                conflicts+=1

        # check other diagonal
        for queen_row, queen_column in enumerate(columns):
            if ((size - queen_column) - queen_row
                == (size - column) - row):
                conflicts+=1
        conflicts-=3 #the queen itself is counted three times
        conflictsArray.append(conflicts)
        
    return conflictsArray



def allZero(thing):
    for item in thing:
        if item != 0: return False
    return True


file_name = "ForwardPropogation2.txt"

text_to_save = ""



for size in range(10, 28):
    num_iterations=0
    number_moves = 0

    listOfIterations = []
    listOfMoves = []
    listOfTimes = []
    for i in range(0, 100):
        columns = [] #columns is the locations for each of the queens
        num_iterations, number_moves, time_taken =dfs_solve_queen(size, True) #forward propogating
        listOfIterations.append(num_iterations)
        listOfMoves.append(number_moves)
        listOfTimes.append(time_taken)
    num_iterations = sum(listOfIterations)/len(listOfIterations)
    number_moves = sum(listOfMoves)/len(listOfMoves)
    time_taken = sum(listOfTimes)/len(listOfTimes)
    myString = "Averages when n was " + str(size) + ": iterations was " + str(num_iterations) + ", moves was " + str(number_moves) + ", time was " + str(time_taken) + "\n"
    print(myString)
    text_to_save += myString


with open(file_name, "w") as file:
    file.write(text_to_save)



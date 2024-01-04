columns = [] #columns is the locations for each of the queens
# columns[r] is a number c if a queen is placed at row r and column c.
size = 8
import random
import time #hint -- you will need this for the following code: column=random.randrange(0,size)

def display():
    for row in range(len(columns)):
        for column in range(size):
            if column == columns[row]:
                print('♛', end=' ')
            else:
                print(' .', end=' ')
        print()


def solve_queen(size):
    tic = time.time()
    columns.clear()
    number_of_moves = 0 #where do I change this so it counts the number of Queen moves?
    number_of_iterations = 0
    row = 0
    column = 0
    # iterate over rows of board
    while True:
        while column < size:
            number_of_iterations+=1
            if next_row_is_safe(column):
                place_in_next_row(column)
                number_of_moves += 1
                row += 1
                column = 0
                break
            else:
                column += 1
        # if I could not find an open column or if board is full
        if (column == size or row == size):
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


# num_iterations, number_moves, time_taken =solve_queen(9)
# print(num_iterations, number_moves, time_taken)
# quit()

fileName = "NormalDFS2.txt"

text_to_save = ""


for size in range(10, 22):
    num_iterations=0
    number_moves = 0

    listOfIterations = []
    listOfMoves = []
    listOfTimes = []
    for i in range(0, 100):
        columns = [] #columns is the locations for each of the queens
        num_iterations, number_moves, time_taken =solve_queen(size)
        listOfIterations.append(num_iterations)
        listOfMoves.append(number_moves)
        listOfTimes.append(time_taken)
    num_iterations = sum(listOfIterations)/len(listOfIterations)
    number_moves = sum(listOfMoves)/len(listOfMoves)
    time_taken = sum(listOfTimes)/len(listOfTimes)
    myString = "Averages when n was " + str(size) + ": iterations was " + str(num_iterations) + ", moves was " + str(number_moves) + ", time was " + str(time_taken) + "\n"
    print(myString)
    text_to_save += myString

with open(fileName, "w") as file:
    file.write(text_to_save)


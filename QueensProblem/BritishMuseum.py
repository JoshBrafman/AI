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


#place_n_queens(size)

def display():
    for row in range(len(columns)):
        for column in range(size):
            if column == columns[row]:
                print('♛', end=' ')
            else:
                print(' .', end=' ')
        print()

def allZero(thing):
    for item in thing:
        if item != 0: return False
    return True

def countConflicts():
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
        conflicts-=3 #each queen counts itself three times
        conflictsArray.append(conflicts)
        
    return conflictsArray

def British():
    tic = time.time()
    iterations = 0
    moves = 0
    while iterations < 50000000:
        iterations+=1
        place_n_queens(size)
        moves += size #or is it 2xsize
        if(allZero(countConflicts())):
            #print("I won even though I'm a monkey on a keyboard!")
            #display()
            return iterations, moves, time.time() - tic
    print("lost")



# Define the file name
britishFile = "britishFile2.txt"

text_to_save = ""

for size in range(7, 11): #I know the table is supposed to start at 10 but I decided to just do 7, 8, and 9 also hopefully that's ok
    num_iterations=0
    number_moves = 0
    listOfIterations = []
    listOfMoves = []
    listOfTimes = []
    for i in range(0, 100):
        columns = [] #columns is the locations for each of the queens
        num_iterations, number_moves, time_taken =British()
        listOfIterations.append(num_iterations)
        listOfMoves.append(number_moves)
        listOfTimes.append(time_taken)
    num_iterations = sum(listOfIterations)/len(listOfIterations)
    number_moves = sum(listOfMoves)/len(listOfMoves)
    time_taken = sum(listOfTimes)/len(listOfTimes)
    myString = "Averages when n was " + str(size) + ": iterations was " + str(num_iterations) + ", moves was " + str(number_moves) + ", time was " + str(time_taken) + "\n"
    print(myString)
    text_to_save += myString



with open(britishFile, "w") as file:
    file.write(text_to_save)


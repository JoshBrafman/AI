import csv
import time
columns = [] #columns is the locations for each of the queens
# columns[r] is a number c if a queen is placed at row r and column c.
size = 4


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


def place_in_next_row(column):
    columns.append(column)

def remove_in_current_row():
    if len(columns) > 0:
        return columns.pop()
    return -1



def countConflicts(): #I ASSUME I DON'T HAVE TO CHANGE MY COUNTERS WITHIN THE FOR LOOPS IN THIS METHOD BECAUSE AS PER PIAZZA "[if] it has nothing to do with placing a queen... it doesn't need to be counted" which was said in the context of forward propogation. I apologize if I am incorrect about that
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


def findLeastConflictsForRow(row, biggest): #biggest was the number of conflicts this queen had
#I ASSUME I DON'T HAVE TO CHANGE MY COUNTERS WITHIN THE FOR LOOPS IN THIS METHOD BECAUSE AS PER PIAZZA "[if] it has nothing to do with placing a queen... it doesn't need to be counted" which was said in the context of forward propogation. I apologize if I am incorrect about that
    conflictsPerCol = []
    for column in range(size):
        conflicts = 0
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
        if column == columns[row]: conflicts-=3 #the queen itself is counted three times
        conflictsPerCol.append(conflicts)

    #print(conflictsPerCol)
    smallest = min(conflictsPerCol)
    #print("smallest I can do", smallest)
    if smallest == biggest: #I can't improve by moving this queen so return -2 (just a random nonsenical number) and False
        return (-2, False)
    indices = [idx for idx, val in enumerate(conflictsPerCol) if val == smallest]
    return (random.choice(indices), True) #I am going to move to a random index that minimizes my conflicts


def climb():
    iterations = 1
    moves = 0
    actualStartTic = time.time()
    place_n_queens(size)
    moves += size
    tic = time.time()
    while True:
        iterations += 1
        conflicts = countConflicts()
        if (all(col == 0 for col in conflicts)):
            # print("won")
            display()
            return iterations,moves, time.time() - actualStartTic
        #display()
        biggest = max(conflicts) #number of conflicts of most problematic queen
        index = conflicts.index(biggest) #where that queen is
        column = -1
        twoNumbers = findLeastConflictsForRow(index, biggest) #twoNumbers is a bad name sorry the first number is the column and the second variable is False if I can't improve by moving this queen
        column = twoNumbers[0] #col to move to to minimize conflicts
        if time.time() - tic < 15 and twoNumbers[1] == True: #I haven't spent a long time on this board already and I can improve my situation by the following move
            columns[index] = column
            moves += 2 #I picked up that row's queen and then moved it
        else:
            tic = time.time() #reset the timer. Note that this is not the timer for the overall time this method took, it's for the if statement above
            #place_n_queens(size)
            colToPut = random.randrange(0,size)
            columns[random.randrange(0,size)] = colToPut #THIS WAS THE KEY!!!! When I reset the whole board here the code took forever to solve. But just moving a random queen to a random column instead of resetting everything worked much better. My logic here was that resetting the whole board makes me lose all of my progress and start over, so I should give the board a little shake but not mess up everything
            moves += 2 # I picked up that random row's queen and then moved it


fileName = "HillClimbing254346.txt"

text_to_save = ""

for size in range(60, 61):
    num_iterations=0
    number_moves = 0

    listOfIterations = []
    listOfMoves = []
    listOfTimes = []
    for i in range(0, 1): #takes a really long time to do 100 so I made it 5
        columns = [] #columns is the locations for each of the queens
        num_iterations, number_moves, time_taken = climb()
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

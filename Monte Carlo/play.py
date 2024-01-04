import game

#play 100 games against the heuristic agent
board=game.game()
game.create(board)
#print("Initial Game 3")
#game.printState(board)
#game.decideWhoIsFirst(board)
game.mcFirst(board) #automatically make mc first. This helps the win rate to be clear, but it also makes it go quicker because it can win faster
comp_count = 0
gameCounter = 0
for i in range(0,100):#This loops takes about 15 seconds on my computer  
    while not game.isFinished(board):
        if game.isHumTurn(board): #The simple agent plays "Human"
            #game.inputMove(board)
            game.inputHeuristic(board) #playing against heuristic
            #game.inputRandom(board)
        else:
            game.inputMC(board) #The MC agent plays "Computer"
        #game.printState(board)
    if game.value(board)==10**20: #the MC Agent won
        comp_count+=1
    #print("Start another game")
    #print(gameCounter)
    #gameCounter += 1
    game.create(board)
    game.mcFirst(board) #automatically make mc first. This helps the win rate to be clear, but it also makes it go quicker because it can win faster
print("The MC agent beat the Heuristic Agent:", comp_count, " out of ", i+1)

#play 100 games against the random agent
print("now playing against random")
board=game.game()
game.create(board)
#print("Initial Game 3")
#game.printState(board)
#game.decideWhoIsFirst(board)
game.mcFirst(board)#automatically make mc first. This helps the win rate to be clear, but it also makes it go quicker because it can win faster
comp_count = 0
for i in range(0,100):#This loops takes about 15 seconds on my computer  
    while not game.isFinished(board):
        if game.isHumTurn(board): #The simple agent plays "Human"
            #game.inputMove(board)
            #game.inputHeuristic(board)
            game.inputRandom(board)
        else:
            game.inputMC(board) #The MC agent plays "Computer"
        #game.printState(board)
    if game.value(board)==10**20: #the MC Agent won
        comp_count+=1
    #print(gameCounter)
    #print(gameCounter)
    gameCounter += 1
    game.create(board)
    game.mcFirst(board)#automatically make mc first. This helps the win rate to be clear, but it also makes it go quicker because it can win faster
print("The MC agent beat the Random agent:", comp_count, " out of ", i+1)



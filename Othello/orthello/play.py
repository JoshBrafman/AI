import alphaBetaPrunning
import game
oneMoreChance = False
board=game.create()
#board = game.createLateStageBoard() this is just here to test end conditions
game.whoIsFirst(board)
while not game.isFinished(board) or oneMoreChance:
    if game.isHumTurn(board):
        game.inputMove(board)
    else:
        board=alphaBetaPrunning.go(board)
    # if (game.isFinished(board)): print("game is finished")
    # print(board)
    if (game.isFinished(board) and not(oneMoreChance)):
        if (game.anyLegalMove(board)):
            print ("No more moves - One more chance")
            game.changePlayer(board)
        else:
            oneMoreChance = False
    else:
        oneMoreChance=False
game.printState(board)


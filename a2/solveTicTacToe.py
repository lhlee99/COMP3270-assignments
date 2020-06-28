#################################################################################
#     File Name           :     solveTicTacToe.py
#     Created By          :     Lee Long Hin 
#     Creation Date       :     [2019-10-16 01:47]
#     Last Modified       :     [2017-03-18 19:17]
#     Description         :      
#################################################################################

import copy
import util 
import sys
import random
import time
from optparse import OptionParser

class GameState:
    """
      Game state of 3-Board Misere Tic-Tac-Toe
      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your search agents. Please do not remove anything, 
      however.
    """
    def __init__(self):
        """
          Represent 3 boards with lists of boolean value 
          True stands for X in that position
        """
        self.boards = [[False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False]]

    def generateSuccessor(self, action):
        """
          Input: Legal Action
          Output: Successor State
        """
        suceessorState = copy.deepcopy(self)
        ASCII_OF_A = 65
        boardIndex = ord(action[0]) - ASCII_OF_A
        pos = int(action[1])
        suceessorState.boards[boardIndex][pos] = True
        return suceessorState

    # Get all valid actions in 3 boards
    def getLegalActions(self, gameRules):
        """
          Input: GameRules
          Output: Legal Actions (Actions not in dead board) 
        """
        ASCII_OF_A = 65
        actions = []
        for b in range(3):
            if gameRules.deadTest(self.boards[b]): continue
            for i in range(9):
                if not self.boards[b][i]:
                    actions.append( chr(b+ASCII_OF_A) + str(i) )
        return actions

    # Print living boards
    def printBoards(self, gameRules):
        """
          Input: GameRules
          Print the current boards to the standard output
          Dead boards will not be printed
        """
        titles = ["A", "B", "C"]
        boardTitle = ""
        boardsString = ""
        for row in range(3):
            for boardIndex in range(3):
                # dead board will not be printed
                if gameRules.deadTest(self.boards[boardIndex]): continue
                if row == 0: boardTitle += titles[boardIndex] + "      "
                for i in range(3):
                    index = 3 * row + i
                    if self.boards[boardIndex][index]: 
                        boardsString += "X "
                    else:
                        boardsString += str(index) + " "
                boardsString += " "
            boardsString += "\n"
        print(boardTitle)
        print(boardsString)

class GameRules:
    """
      This class defines the rules in 3-Board Misere Tic-Tac-Toe. 
      You can add more rules in this class, e.g the fingerprint (patterns).
      However, please do not remove anything.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        {}
        
    def deadTest(self, board):
        """
          Check whether a board is a dead board
        """
        if board[0] and board[4] and board[8]:
            return True
        if board[2] and board[4] and board[6]:
            return True
        for i in range(3):
            #check every row
            row = i * 3
            if board[row] and board[row+1] and board[row+2]:
                return True
            #check every column
            if board[i] and board[i+3] and board[i+6]:
                return True
        return False

    def isGameOver(self, boards):
        """
          Check whether the game is over  
        """
        return self.deadTest(boards[0]) and self.deadTest(boards[1]) and self.deadTest(boards[2])
    
    def getPattern(self, board):
        """
          Get the Pattern
        """
        def generatePattern(id):
            board = [False, False, False, False, False, False, False, False, False]
            for i in range(len(id)):
                board[int(id[i])] = True
            return board

        pattern = [ 
            (2, ["013578", "01568", "01567", "01456", "1357", "0268", "0178", "0138", "0135", "0134", "045", "027", "024", "016", "17", "13", "08"]),
            (3, ["02", "04", "05", "14", "013", "315", "0145", "0146", "0156", "0167", "0168", "0247", "0457", "01357", "01358"]),
            (5, [""]),
            (25, ["4"]),
            (11, ["017", "018", "015"]),
            (13, ["01"]),
            (17, ["014", "026", "134", "0157", "0158"]),
            (1, ["0", "1", "057"]) 
            ]

        if self.deadTest(board):
            return 1
        for p in pattern:
            for i in p[1]:
                if self.deepEq( generatePattern(i), board ):
                    return p[0]
        print(board)
        print()
        return "Error"     

    def fullPattern(self, boards):
        return self.getPattern(boards[0]) * self.getPattern(boards[1]) * self.getPattern(boards[2])

    def eq(self, board1, board2):
        """
          Check if 2 boards are completely the same
        """
        equal = (board1[0] == board2[0] and board1[1] == board2[1] and
                board1[2] == board2[2] and board1[3] == board2[3] and
                board1[4] == board2[4] and board1[5] == board2[5] and
                board1[6] == board2[6] and board1[7] == board2[7] and
                board1[8] == board2[8])
        return equal

    def transform(self, board, xy):
        """
          Return a x/y-filpped board or rotated(90 degree, clockwise) board
        """
        tmp = list(board)
        if xy == 'x':
            for i in range(3):
                tmp[i*3] = board[i*3 + 2]
                tmp[i*3 + 2] = board[i*3]
        elif xy == 'y':
            for i in range(3):
                tmp[i] = board[i + 6]
                tmp[i + 6] = board[i]
        elif xy == 'r':
            tmp[0] = board[6]
            tmp[1] = board[3]
            tmp[2] = board[0]
            tmp[3] = board[7]
            tmp[4] = board[4]
            tmp[5] = board[1]
            tmp[6] = board[8]
            tmp[7] = board[5]
            tmp[8] = board[2]
        return tmp        

    def deepEq(self, board1, board2):
        """
          Check if 2 boards are completely the same after rotation and reflection
        """
        for i in range(4):
            if self.eq(board1, board2) or self.eq(self.transform(board1, 'x'), board2):
                return True
            board1 = self.transform(board1, 'r')
        return False
        

class TicTacToeAgent():
    """
      When move first, the TicTacToeAgent should be able to chooses an action to always beat 
      the second player.

      You have to implement the function getAction(self, gameState, gameRules), which returns the 
      optimal action (guarantee to win) given the gameState and the gameRules. The return action
      should be a string consists of a letter [A, B, C] and a number [0-8], e.g. A8. 

      You are welcome to add more helper functions in this class to help you. You can also add the
      helper function in class GameRules, as function getAction() will take GameRules as input.
      
      However, please don't modify the name and input parameters of the function getAction(), 
      because autograder will call this function to check your algorithm.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        {}

    def getAction(self, gameState, gameRules):
        def lessActions(gameState):
            actions = gameState.getLegalActions(gameRules)
            lessActions = []
            pattern = ['a', 'b', 'c', 'c2', 'd', 'ad', 'ab', '1']
            existPattern = []
            currentPattern = gameRules.fullPattern(gameState.boards)
            for a in actions:
                if gameRules.fullPattern(gameState.generateSuccessor(a).boards) not in existPattern:
                    existPattern.append(gameRules.fullPattern(gameState.generateSuccessor(a).boards))
                    lessActions.append(a)
            return lessActions

        def miniMax(gameState, agentIndex, alpha, beta, depth):
            depth += 1 
            
            if agentIndex >= 2:
                agentIndex = 0
            
            if gameRules.isGameOver(gameState.boards):
                if agentIndex == 0:
                    return [2]
                else:
                    return [-2]
            if depth >= 4:
                pattern = gameRules.fullPattern(gameState.boards)
                # print("leave: {}".format(pattern))

                if pattern in [25, 2, 9, 15]:
                    return [2]
                else:
                    return [-2]

            v1 = (-float("inf"), '/')
            v2 = (float("inf"), '/')
            actions = lessActions(gameState)
            # print(agentIndex,depth, actions)
            for a in actions:
                nextState = miniMax( gameState.generateSuccessor(a), agentIndex + 1, alpha, beta, depth)
                # print(nextState)
                if agentIndex == 0:
                    v1 = (v1) if v1[0] > nextState[0] else (nextState[0], a)
                    if v1[0] > beta:
                        return v1
                    alpha = max(alpha, v1[0])
            
                else:
                    v2 = (v2) if v2[0] < nextState[0] else (nextState[0], a)
                    if v2[0] < alpha:
                        return v2
                    beta = min(beta, v2[0])

            tmp = v1 if agentIndex == 0 else v2
            
            return tmp

        tmp = miniMax(gameState, 0, -float("inf"), float("inf"), 0)
        return tmp[1]
        # currentState.generateSuccessor(action)



class randomAgent():
    """
      This randomAgent randomly choose an action among the legal actions
      You can set the first player or second player to be random Agent, so that you don't need to
      play the game when debugging the code. (Time-saving!)
      If you like, you can also set both players to be randomAgent, then you can happily see two 
      random agents fight with each other.
    """
    def getAction(self, gameState, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return random.choice(actions)


class keyboardAgent():
    """
      This keyboardAgent return the action based on the keyboard input
      It will check whether the input actions is legal or not.
    """
    def checkUserInput(self, gameState, action, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return action in actions

    def getAction(self, gameState, gameRules):
        action = input("Your move: ")
        while not self.checkUserInput(gameState, action, gameRules):
            print("Invalid move, please input again")
            action = input("Your move: ")
        return action 

class Game():
    """
      The Game class manages the control flow of the 3-Board Misere Tic-Tac-Toe
    """
    def __init__(self, numOfGames, muteOutput, randomAI, AIforHuman):
        """
          Settings of the number of games, whether to mute the output, max timeout
          Set the Agent type for both the first and second players. 
        """
        self.numOfGames  = numOfGames
        self.muteOutput  = muteOutput
        self.maxTimeOut  = 30 

        self.AIforHuman  = AIforHuman
        self.gameRules   = GameRules()
        self.AIPlayer    = TicTacToeAgent()

        if randomAI:
            self.AIPlayer = randomAgent()
        else:
            self.AIPlayer = TicTacToeAgent()
        if AIforHuman:
            self.HumanAgent = randomAgent()
        else:
            self.HumanAgent = keyboardAgent()

    def run(self):
        """
          Run a certain number of games, and count the number of wins
          The max timeout for a single move for the first player (your AI) is 30 seconds. If your AI 
          exceed this time limit, this function will throw an error prompt and return. 
        """
        numOfWins = 0;
        for i in range(self.numOfGames):
            gameState = GameState()
            agentIndex = 0 # 0 for First Player (AI), 1 for Second Player (Human)
            while True:
                if agentIndex == 0: 
                    timed_func = util.TimeoutFunction(self.AIPlayer.getAction, int(self.maxTimeOut))
                    try:
                        start_time = time.time()
                        action = timed_func(gameState, self.gameRules)
                    except util.TimeoutFunctionException:
                        print("ERROR: Player %d timed out on a single move, Max %d Seconds!" % (agentIndex, self.maxTimeOut))
                        return False

                    if not self.muteOutput:
                        print("Player 1 (AI): %s" % action)
                else:
                    action = self.HumanAgent.getAction(gameState, self.gameRules)
                    if not self.muteOutput:
                        print("Player 2 (Human): %s" % action)
                gameState = gameState.generateSuccessor(action)
                if self.gameRules.isGameOver(gameState.boards):
                    break
                if not self.muteOutput:
                    gameState.printBoards(self.gameRules)

                agentIndex  = (agentIndex + 1) % 2
            if agentIndex == 0:
                print("****player 2 wins game %d!!****" % (i+1))
            else:
                numOfWins += 1
                print("****Player 1 wins game %d!!****" % (i+1))

        print("\n****Player 1 wins %d/%d games.**** \n" % (numOfWins, self.numOfGames))


if __name__ == "__main__":
    """
      main function
      -n: Indicates the number of games
      -m: If specified, the program will mute the output
      -r: If specified, the first player will be the randomAgent, otherwise, use TicTacToeAgent
      -a: If specified, the second player will be the randomAgent, otherwise, use keyboardAgent
    """
    # Uncomment the following line to generate the same random numbers (useful for debugging)
    #random.seed(1)  
    parser = OptionParser()
    parser.add_option("-n", dest="numOfGames", default=1, type="int")
    parser.add_option("-m", dest="muteOutput", action="store_true", default=False)
    parser.add_option("-r", dest="randomAI", action="store_true", default=False)
    parser.add_option("-a", dest="AIforHuman", action="store_true", default=False)
    (options, args) = parser.parse_args()
    ticTacToeGame = Game(options.numOfGames, options.muteOutput, options.randomAI, options.AIforHuman)
    ticTacToeGame.run()

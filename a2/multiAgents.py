from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        h = 0
        # if no scare time
        # find capsules
        if successorGameState.getCapsules():
          cDistance = []
          for i in successorGameState.getCapsules():
            cDistance.append(manhattanDistance(newPos, i))
          cDistance = min(cDistance)
          h -= cDistance * 2

        # stay away from ghost
        
        for i in newGhostStates:
          if manhattanDistance(newPos, i.getPosition()) <= 1:
            h -= 100
          # gDistance += manhattanDistance(newPos, i.getPosition())

        # find food
        fDistance = []
        for x in range(prevFood.width):
          for y in range(prevFood.height):
            if prevFood[x][y]:
              fDistance.append( manhattanDistance(newPos,(x,y)) )
        h -= min(fDistance)
        
        # if scare time
        # print(newScaredTimes, type(newScaredTimes))
        if newScaredTimes[0] != 0:
          gDistance = []
          for i in newGhostStates:
            gDistance.append(manhattanDistance(newPos, i.getPosition()))
            if min(gDistance) < newScaredTimes[0]:
              return -min(gDistance) 
        return h
        

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def miniMax(gameState, agentIndex, depth):
          if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            depth += 1
            
          if depth == self.depth or gameState.isWin() or gameState.isLose():
            return [self.evaluationFunction(gameState)]
          
          actions = gameState.getLegalActions(agentIndex)
          nextValue = []
          corrsAction = []
          for a in actions:
            nextValue.append( miniMax( gameState.generateSuccessor(agentIndex, a), agentIndex + 1, depth )[0] )
            corrsAction.append(a)
          
          for i in range(len(nextValue)):
            if agentIndex == 0:
              if max(nextValue) == nextValue[i]:
                return [max(nextValue), corrsAction[i]]
            else:
              if min(nextValue) == nextValue[i]:
                return [min(nextValue), corrsAction[i]]

        
        return miniMax(gameState, 0, 0)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        def miniMax(gameState, agentIndex, depth, alpha, beta):
          if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            depth += 1
            
          if depth == self.depth or gameState.isWin() or gameState.isLose():
            return [self.evaluationFunction(gameState)]
          
          actions = gameState.getLegalActions(agentIndex)
          v1 = (-float("inf"), '/')
          v2 = (float("inf"), '/')
          for a in actions: 
            nextState = miniMax( gameState.generateSuccessor(agentIndex, a), agentIndex + 1, depth, alpha, beta ) 
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

        return miniMax(gameState, 0, 0, -float("inf"), float("inf"))[1]
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        def miniMax(gameState, agentIndex, depth):
          if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            depth += 1
            
          if depth == self.depth or gameState.isWin() or gameState.isLose():
            return [self.evaluationFunction(gameState)]
          
          actions = gameState.getLegalActions(agentIndex)
          nextValue = []
          corrsAction = []
          for a in actions:
            nextValue.append( miniMax( gameState.generateSuccessor(agentIndex, a), agentIndex + 1, depth )[0] )
            corrsAction.append(a)
          
          expectedValue = 0
          for i in range(len(nextValue)):
            if agentIndex == 0:
              if max(nextValue) == nextValue[i]:
                return [max(nextValue), corrsAction[i]]
            else:
              expectedValue += nextValue[i] / len(nextValue)
          return [expectedValue]
        
        return miniMax(gameState, 0, 0)[1]


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: The evaluation function have 2 modes:
                      1. when pacman is normal
                        Pacman should try to eat all the food and power pellet and avoid losing. 
                        The function will return
                          currentScore - numberOfFood - distanceToClosestFood - 10000(if pacman is too close to the ghost)

                      2. when pacman is powered up
                        Pacman should try to chase the ghost.
                        The function will return
                          currentScore - distanceToClosestGhost

    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)
    prevFood = currentGameState.getFood()
    pacPos = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    "Not Powered up"
    val = 0
    # stay away from ghost
    for i in ghostStates:
      if manhattanDistance(pacPos, i.getPosition()) <= 1:
        val -= 10000

    # Food
    fDistance = []
    for x in range(prevFood.width):
      for y in range(prevFood.height):
        if prevFood[x][y]:
          if manhattanDistance(pacPos,(x,y)) == 1:
            fDistance.append(1)
          else:
            fDistance.append( manhattanDistance(pacPos,(x,y)) )

    # Power pellet are treated as food
    [ fDistance.append(manhattanDistance(pacPos, i)) for i in currentGameState.getCapsules() ]
    
    # avoid error when there is no food or power pellet
    if not fDistance:
      fDistance.append(0)

    # number of remaining food (power pellet not included)
    numberOfFood = currentGameState.getNumFood()
    
    # the final equation
    val += currentGameState.getScore() - min(fDistance) - numberOfFood

    "Powered up"
    # chase the closest ghost if pacman is powered up
    if scaredTimes[0] != 0:
      gDistance = []
      for i in ghostStates:
        gDistance.append(manhattanDistance(pacPos, i.getPosition()))
      return currentGameState.getScore() - min(gDistance)

    return val

# Abbreviation
better = betterEvaluationFunction


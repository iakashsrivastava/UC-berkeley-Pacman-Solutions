# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


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
#    successorGameState = currentGameState.generatePacmanSuccessor(action)
#    newPos = successorGameState.getPacmanPosition()
#    newFood = successorGameState.getFood()
#    newGhostStates = successorGameState.getGhostStates()
#    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
##        if action == 'Stop':
##            return 0
##        # Useful information you can extract from a GameState (pacman.py)
##        successorGameState = currentGameState.generatePacmanSuccessor(action)
##        #print successorGameState
##        newPos = successorGameState.getPacmanPosition()
##        #print "a"
##        #for i in newPos:
###            print i
##        newFood = successorGameState.getFood()
##        newFood = newFood.asList()
###        for n in newFood:
###            print n
##        #print newFood
##        newGhostStates = successorGameState.getGhostStates()
###        print "a"
###        for j in newGhostStates:
## #           print j.getPosition()
##        
##        #for g in newGhostStates:
###            print g.getPosition()
##        foodDistance = []
        "*** YOUR CODE HERE ***"
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()  
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        if Directions.STOP in action:  
            return -10000
        
        for ghostState in newGhostStates:
          ghostPos = ghostState.getPosition()
          if ghostPos == newPos and ghostState.scaredTimer == 0:
                return -10000

        foodlocs = currentGameState.getFood().asList()
        for food in foodlocs:
          dis = [manhattanDistance(food,newPos)]
    #    print dis
    #    if max(man_dis) == 0:
    #      return 0
        #else:
        return (-max(dis))
 #           "*** YOUR CODE HERE ***"
#            return successorGameState.getScore()

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
    def minimax(self, gameState, depth, agentIndex):
        
        if (gameState.isWin() or gameState.isLose()):
            return (self.evaluationFunction(gameState))
        best_action=''
        
        if (agentIndex==0):
            best_value = -1000000
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
          #      if action != Directions.STOP:
                    node = gameState.generateSuccessor(agentIndex, action)
                    val = self.minimax(node, depth, agentIndex+1)
                    if (best_value < val):
                        best_value = val
                        best_action = action
            if (depth == 1):
                return best_action
          #  else:
           #     return best_value
        else:
            best_value = 1000000
            agents = gameState.getNumAgents()
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
               # if action != Directions.STOP:
                    node = gameState.generateSuccessor(agentIndex, action)
                    if agentIndex == agents - 1:
                        if(depth == self.depth):
                            val = self.evaluationFunction(node)
                        else:
                            val = self.minimax(node, depth+1, 0)
                    else:
                        val = self.minimax(node, depth, agentIndex+1)
                    if best_value > val:
                        best_value = val
                        best_action = action
        return best_value
                       
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
        """
        "*** YOUR CODE HERE ***"
        
        return (self.minimax(gameState,1, 0))

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def alphabeta(self, gameState, depth, agentIndex,alpha ,beta):
        
        if (gameState.isWin() or gameState.isLose()):
            return (self.evaluationFunction(gameState))
        best_action=''
        
        if (agentIndex==0):
            best_value = -1000000
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
          #      if action != Directions.STOP:
                    node = gameState.generateSuccessor(agentIndex, action)
                    val = self.alphabeta(node, depth, agentIndex+1, alpha ,beta)
                    if (val > beta):
                        return val
                    if (val > best_value):
                        best_value = val
                        best_action = action
                        
                    alpha = max(alpha, best_value)

            if (depth == 1):
                return best_action
          #  else:
           #     return best_value
        else:
            best_value = 1000000
            agents = gameState.getNumAgents()
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
               # if action != Directions.STOP:
                    node = gameState.generateSuccessor(agentIndex, action)
                    if (agentIndex == agents - 1):
                        if(depth == self.depth):
                            val = self.evaluationFunction(node)
                        else:
                            val = self.alphabeta(node, depth+1, 0, alpha, beta)
                    else:
                        val = self.alphabeta(node, depth, agentIndex+1,alpha ,beta)
                    
                    if (val < alpha):
                        return val
                    
                    if (val < best_value):
                        best_value = val
                        best_action = action
                        
                    beta = min(beta, best_value)
                        
        return best_value
                       
    def getAction(self, gameState):
        "*** YOUR CODE HERE ***"
        alpha = -10000000
        beta = +10000000
        
        return (self.alphabeta(gameState,1 , 0, alpha, beta))

class ExpectimaxAgent(MultiAgentSearchAgent):

    def expectimax(self, gameState, depth, agentIndex):
        
        if (gameState.isWin() or gameState.isLose()):
            return (self.evaluationFunction(gameState))
        best_action=''
        expecti_val = 0
        
        if (agentIndex==0):
            best_value = -1000000
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
          #      if action != Directions.STOP:
                    node = gameState.generateSuccessor(agentIndex, action)
                    val = self.expectimax(node, depth, agentIndex+1)
                    if (best_value < val):
                        best_value = val
                        best_action = action
            if (depth == 1):
                return best_action
            else:
                return best_value
        else:
            agents = gameState.getNumAgents()
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
               # if action != Directions.STOP:
                    node = gameState.generateSuccessor(agentIndex, action)
                    if agentIndex == agents - 1:
                        if(depth == self.depth):
                            val = self.evaluationFunction(node)
                        else:
                            val = self.expectimax(node, depth+1, 0)
                    else:
                        val = self.expectimax(node, depth, agentIndex+1)
                    expecti_val = expecti_val + (val/len(actions))
            return expecti_val 
                       
    def getAction(self, gameState):
        
        return (self.expectimax(gameState,1, 0))

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: calculated the minimum possible ghost distance & food distance and calculated the heuristic accordingly 
    """
    newFood = currentGameState.getFood().asList()
    newPos = currentGameState.getPacmanPosition()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    minFoodDist = 1000000
    minGhostDist = 1000000
        
    for ghostState in newGhostStates:
        ghostPos = ghostState.getPosition()
        minGhostDist = min(minGhostDist,(manhattanDistance(ghostPos,newPos)))
        
    for newScaredTime in newScaredTimes:
        minGhostDist += newScaredTime
       
    for foodloc in newFood:
        minFoodDist = min(minFoodDist,(manhattanDistance(foodloc,newPos)))
        
    inverseFoodDist=1.0/minFoodDist 
        
    return ((minGhostDist*(inverseFoodDist**3)) + currentGameState.getScore())
        
# Abbreviation
better = betterEvaluationFunction
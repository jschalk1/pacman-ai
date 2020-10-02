# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
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
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #get the current position of pacman
        position = list(successorGameState.getPacmanPosition())

        #set the lowest to very low number to be used for comparing
        lowest = 1e6
        dist = 0

        #get all the current food in the game state
        food = currentGameState.getFood().asList()
        #loop through all the food in game state
        for a in range(len(food)):
            #get the distance between the position and the food in game state 
            dist = (manhattanDistance(food[a], position))
            #if the distance to the food is less than the lowest set the lowest equal to the distance
            if dist < lowest:
                lowest = dist
        #change sign on lowest to reflect the inverse of the distance of the food
        lowest = -lowest
        #if theres a ghost at position then return max negative to avoid
        for gState in newGhostStates:
            if gState.scaredTimer == 0 and gState.getPosition() == tuple(position):
                return -1e6

        #if we get the stop action then return max neg to keep moving
        if action == 'Stop':
            return -1e6
        return lowest

        

        # return successorGameState.getScore()

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
        """
        "*** YOUR CODE HERE ***"
        #define function
        def minimax(gState, depth, player):
            #check if min layer
            if player == gState.getNumAgents():
                #check if at max depth
                if depth == self.depth:
                    #evaluate gamestate
                    return self.evaluationFunction(gState)
                else:
                    #recurse and increase depth
                    return minimax( gState, depth + 1, 0 )
            else:
                #get available actions
                actions = gState.getLegalActions(player)
                #if no actions then evaluate the game state
                if len(actions) == 0:
                    return self.evaluationFunction(gState)
                
                #get the minimax values for the next layer 
                fut =( minimax(gState.generateSuccessor(player, a), depth, player+1) for a in actions)

                #either return min on max based on player
                if player == 0:
                    return max(fut)
                else:
                    return min(fut)    
        #return the action that has the max minimax value        
        ans = max(gameState.getLegalActions(0), key = lambda x: minimax(gameState.generateSuccessor(0,x),1,1))

        return ans



        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def  minValue(gState, player, depth, a, b):
            #store number of agents and legal actions by the player
            playerCount = gameState.getNumAgents()
            actions = gState.getLegalActions(player)

            #if there are no actions then return the eval function
            if not actions:
                return self.evaluationFunction(gState)
            #initialize the lowest value 
            lowestValue = 1e6
            beta = b

            #pacmans turn to move
            if player == playerCount -1:
                #loop through all legal actions
                for action in actions:
                    #get the mininmum of the lowestValue variable and the max value of the current state
                    lowestValue = min(lowestValue, maxValue(gState.generateSuccessor(player, action), player, depth, a, beta))
                    #if lowestValue is less than alpha than return the lowest value
                    if lowestValue < a:
                        return lowestValue
                    #get the min of beta and lowestValue and reinit beta with the min
                    beta = min(beta, lowestValue)
            else:
                #loop through all legal actions
                for action in actions:
                    #get the mininmum of the lowestValue variable and the min value of the current state
                    lowestValue = min(lowestValue, minValue(gState.generateSuccessor(player, action), player+1, depth, a, beta))
                    #check the new lowest value and if its less than alpha return
                    if lowestValue < a:
                        return lowestValue
                    #set beta to the minimum of beta and the min value
                    beta = min(beta, lowestValue)
            return lowestValue

        
        def maxValue(gState, player, depth, a, b):
            #set player to 0 since maxValue will be used for pacman
            player = 0
            actions = gState.getLegalActions(player)

            #same check as in minValue but now we check for depth also
            if not actions or depth == self.depth:
                return self.evaluationFunction(gState)

            #init the highest value
            highestValue = -1e6
            alpha = a
            #loop through all legal actions
            for action in actions:
                #get the maximum of the highestValue variable and the max value of the current state
                highestValue = max(highestValue, minValue(gState.generateSuccessor(player, action), player +1, depth+1, alpha, b))
                #if highestValue is greater than beta return
                if highestValue > b:
                    return highestValue
                #set alpha to the maximum of alpha and the highest value
                alpha = max(alpha, highestValue)
            return highestValue

        #trying to find the best possible moves for pacman (player 0)
        actions = gameState.getLegalActions(0)
        #init alpha beta
        a = -1e6
        b = 1e6

        #init list for all actions
        everyAction = {}
        #loop through all legal actions for pacman
        for action in actions:
            #run minValue and save the value
            value = minValue(gameState.generateSuccessor(0, action), 1, 1, a, b)
            #populate the list with minValues for all actions
            everyAction[action] = value

            #update the alpha var
            if value > b:
                return a
            a = max(value, a)

        return max(everyAction, key=everyAction.get)




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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction


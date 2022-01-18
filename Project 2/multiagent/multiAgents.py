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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        minGhostDist = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = successorGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDist = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDists = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDist = 0 if not newFoodsDists else min(newFoodsDists)
        isFoodNearer = nearestFoodDist - newNearestFoodDist

        direction = currentGameState.getPacmanState().getDirection()

        ret_val = 0
        if minGhostDist <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            ret_val = 8
        elif isFoodNearer > 0:
            ret_val = 4
        elif action == direction:
            ret_val = 2
        else:
            return 1
        return ret_val



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
        numberOfGhosts = gameState.getNumAgents() - 1

        def maxValue(gameState,depth):
            currDepth = depth + 1
            if gameState.isWin() or gameState.isLose() or currDepth==self.depth: 
                return self.evaluationFunction(gameState)
            maxvalue = -999999
            actions = gameState.getLegalActions(0)
            for action in actions:
                successor= gameState.generateSuccessor(0,action)
                maxvalue = max (maxvalue,minValue(successor,currDepth,1))
            return maxvalue
        
        def minValue(gameState,depth, agentIndex):
            minvalue = 999999
            if gameState.isWin() or gameState.isLose():    
                return self.evaluationFunction(gameState)
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
                successor= gameState.generateSuccessor(agentIndex,action)
                if agentIndex == (gameState.getNumAgents() - 1):
                    minvalue = min (minvalue,maxValue(successor,depth))
                else:
                    minvalue = min(minvalue,minValue(successor,depth,agentIndex+1))
            return minvalue
        
        actions = gameState.getLegalActions(0)
        currentScore = -999999
        returnAction = ''
        for action in actions:
            nextState = gameState.generateSuccessor(0,action)
            score = minValue(nextState,0,1)
            if score > currentScore:
                returnAction = action
                currentScore = score
        return returnAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def maxValue(gameState,depth,alpha, beta):
            currDepth = depth + 1
            if gameState.isWin() or gameState.isLose() or currDepth==self.depth:    
                return self.evaluationFunction(gameState)
            maxvalue = -999999
            actions = gameState.getLegalActions(0)
            alpha1 = alpha
            for action in actions:
                successor= gameState.generateSuccessor(0,action)
                maxvalue = max (maxvalue,minValue(successor,currDepth,1,alpha1,beta))
                if maxvalue > beta:
                    return maxvalue
                alpha1 = max(alpha1,maxvalue)
            return maxvalue
        
        def minValue(gameState,depth,agentIndex,alpha,beta):
            minvalue = 999999
            if gameState.isWin() or gameState.isLose():   
                return self.evaluationFunction(gameState)
            actions = gameState.getLegalActions(agentIndex)
            beta1 = beta
            for action in actions:
                successor= gameState.generateSuccessor(agentIndex,action)
                if agentIndex == (gameState.getNumAgents()-1):
                    minvalue = min (minvalue,maxValue(successor,depth,alpha,beta1))
                    if minvalue < alpha:
                        return minvalue
                    beta1 = min(beta1,minvalue)
                else:
                    minvalue = min(minvalue,minValue(successor,depth,agentIndex+1,alpha,beta1))
                    if minvalue < alpha:
                        return minvalue
                    beta1 = min(beta1,minvalue)
            return minvalue

        actions = gameState.getLegalActions(0)
        currentScore = -999999
        returnAction = ''
        alpha = -999999
        beta = 999999
        for action in actions:
            nextState = gameState.generateSuccessor(0,action)
            score = minValue(nextState,0,1,alpha,beta)
            if score > currentScore:
                returnAction = action
                currentScore = score
            if score > beta:
                return returnAction
            alpha = max(alpha,score)
        return returnAction



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

        def maxValue(state, depth):
            legalActions = state.getLegalActions(0)
            if not legalActions or depth == self.depth:
                return self.evaluationFunction(state)

            v = max(expValue(state.generateSuccessor(0, action), 0 + 1, depth + 1) for action in legalActions)
            return v

        def expValue(state, agentIndex, depth):
            legalActions = state.getLegalActions(agentIndex)
            if not legalActions:
                return self.evaluationFunction(state)

            probability = 1.0 / len(legalActions)
            v = 0
            for action in legalActions:
                newState = state.generateSuccessor(agentIndex, action)
                if agentIndex == state.getNumAgents() - 1:
                    v += maxValue(newState, depth) * probability
                else:
                    v += expValue(newState, agentIndex + 1, depth) * probability
            return v

        legalActions = gameState.getLegalActions()
        bestAction = max(legalActions, key=lambda action: expValue(gameState.generateSuccessor(0, action), 1, 1))
        return bestAction

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    
    foodList = newFood.asList()
    foodDist = [0]
    for pos in foodList:
        foodDist.append(manhattanDistance(newPos,pos))

    ghostPos = []
    for ghost in newGhostStates:
        ghostPos.append(ghost.getPosition())
    ghostDist = [0]
    for pos in ghostPos:
        ghostDist.append(manhattanDistance(newPos,pos))

    numberofPowerPellets = len(currentGameState.getCapsules())

    score = 0
    numberOfNoFoods = len(newFood.asList(False))           
    sumScaredTimes = sum(newScaredTimes)
    sumGhostDist = sum (ghostDist)
    reciprocalfoodDist = 0
    if sum(foodDist) > 0:
        reciprocalfoodDist = 1.0 / sum(foodDist)
        
    score += currentGameState.getScore()  + reciprocalfoodDist + numberOfNoFoods

    if sumScaredTimes > 0:    
        score +=   sumScaredTimes + (-1 * numberofPowerPellets) + (-1 * sumGhostDist)
    else :
        score +=  sumGhostDist + numberofPowerPellets
    return score

# Abbreviation
better = betterEvaluationFunction
